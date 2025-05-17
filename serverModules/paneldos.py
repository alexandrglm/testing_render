from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, abort, send_from_directory
from functools import wraps
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import psutil
import requests
import time
from serverModules.panel_modules import start_module
import json

from flask import current_app

load_dotenv()

admin_panel = Blueprint('admin_panel', __name__, template_folder='templates')

ADMIN_SECRETS = os.getenv('ADMIN_SECRETS')
ADMIN_HASH = os.getenv('ADMIN_HASH')
ADMIN_SESSION_TIMEOUT = int(os.getenv('ADMIN_SESSION_TIMEOUT', '1800'))
UPTIMEROBOT_API_KEY = os.getenv("UPTIMEROBOT_API_KEY")

ADMIN_SESSION = {
    'is_admin': False,
    'last_activity': None,
    'timeout': ADMIN_SESSION_TIMEOUT
}

SERVER_MODULES = {
    'logs': {'enabled': True},
    'mail': {'enabled': True},
    'nukebots': {'enabled': True},
    'telegram': {'enabled': True},
    'keep': {'enabled': True},
}

valid_modules = [
    'dashboard_module.html',
    'stats_module.html',
    'secrets_module.html',
    'services_module.html'  # <- Agregado
]

###############################################
# ADMIN ALOWED DECORATOR
def admin_required(f):

    @wraps(f)
    
    def decorated_function(*args, **kwargs):
    
    
        if not validate_admin_session():
    
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Admin access required'}), 403
    
            return redirect(url_for('admin_panel.login'))
    
        return f(*args, **kwargs)
    
    return decorated_function

###############################################
# ADMIN COOKIE SESSION VLAIDATION
def validate_admin_session():

    if ADMIN_SESSION['is_admin']:
    
        now = datetime.now()
    
        last_activity = ADMIN_SESSION['last_activity']
    
    
        if last_activity and (now - last_activity).total_seconds() > ADMIN_SESSION['timeout']:
    
            ADMIN_SESSION['is_admin'] = False
            return False
    
    
        ADMIN_SESSION['last_activity'] = now
    
    return ADMIN_SESSION['is_admin']

###############################################
# ADMIN LOGIN PATH
@admin_panel.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
    
        password = request.form.get('password')
    
        if not password or not ADMIN_HASH:
    
            return jsonify({'error': 'No password or hash set'}), 500
    
    
        from werkzeug.security import check_password_hash
    
    
        if not check_password_hash(ADMIN_HASH, password):
    
            return jsonify({'error': 'Incorrect Password!'}), 401
    
    
        ADMIN_SESSION.update({
            'is_admin': True,
            'last_activity': datetime.now()
        })
    
    
        return jsonify({'redirect': url_for('admin_panel.panel'), 'status': 'success'})
    
    
    return render_template('admin/login.html')

###############################################
# ADMIN LOGOUT, pending fixes

@admin_panel.route('/logout', methods=['POST'])

def logout():

    ADMIN_SESSION.update({'is_admin': False, 'last_activity': None})

    return jsonify({'redirect': url_for('admin_panel.login')})



###############################################
# ADMIN panel route
@admin_panel.route('/')
@admin_required
def panel():

    return render_template('admin/panel.html')



###############################################
# CHEKING ADMIN fetch for front
@admin_panel.route('/api/check-auth')

def check_auth():

    return jsonify({
        'is_admin': validate_admin_session(),
        'timeout': ADMIN_SESSION_TIMEOUT - (datetime.now() - ADMIN_SESSION['last_activity']).total_seconds()
                    if ADMIN_SESSION['last_activity'] else 0
    })

###############################################
# PANEL SYSTEM STATS API
@admin_panel.route('/api/system-stats')
@admin_required
def system_stats():
    
    uptime_seconds = int(time.time() - psutil.boot_time())
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60

    return jsonify({
        'status': 'success',
        'cpu': {
            'percent': psutil.cpu_percent(),
            'cores': psutil.cpu_count(),
            'load': [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
        },
        'memory': {
            'total': psutil.virtual_memory().total,
            'used': psutil.virtual_memory().used,
            'percent': psutil.virtual_memory().percent
        },
        'disk': {
            'total': psutil.disk_usage('/').total,
            'used': psutil.disk_usage('/').used,
            'percent': psutil.disk_usage('/').percent
        },
        'uptime': {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': uptime_seconds,
            'formatted': f"{days}d {hours}h {minutes}m"
        }
    })
###############################################
# PANEL ADMIN -> SECRETS MANAGING
@admin_panel.route('/api/secrets-list')
@admin_required
def secrets_list():

    secrets = []
    
    
    for f in os.listdir(ADMIN_SECRETS):
    
        if f.endswith(('.json', '.txt', '.env', '.html')):
            file_path = os.path.join(ADMIN_SECRETS, f)
    
            if os.path.isfile(file_path):
    
                stat = os.stat(file_path)
    
                secrets.append({
                    'name': f,
                    'size': stat.st_size,
                    'modified': stat.st_mtime,
                    'formatted_size': format_file_size(stat.st_size),
                    'formatted_date': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
    
    
    return jsonify({'status': 'success', 'secrets': secrets})


# FILESIZES HELPER
def format_file_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} GB"


# GETTING SECRET FILES
@admin_panel.route('/api/secrets/<filename>')
@admin_required

def secret_content(filename):

    if not filename or '..' in filename or filename.startswith('/'):
        abort(400)


    secret_path = os.path.join(ADMIN_SECRETS, filename)


    if not os.path.isfile(secret_path):

        abort(404)

    return send_from_directory(ADMIN_SECRETS, filename, as_attachment=False, mimetype='text/plain')

###############################################
# PANEL ADMIN -> GET MODULES FROM SECRETS
@admin_panel.route('/api/module/<module_name>')
@admin_required
def get_admin_module(module_name):

    if module_name not in valid_modules:
        abort(404)
    
    path = os.path.join(ADMIN_SECRETS, module_name)
    
    
    if not os.path.isfile(path):
    
        abort(404)
    
    
    
    with open(path, 'r', encoding='utf-8') as f:
    
        return f.read()

###############################################
# PANEL ADMIN -> UPTIMESTATS ROBOT API

@admin_panel.route('/api/uptime-stats')
@admin_required
def uptime_robot_stats():

    if not UPTIMEROBOT_API_KEY:
        return jsonify({'status': 'error', 'message': 'API key missing'}), 500


    response = requests.post(
        'https://api.uptimerobot.com/v2/getMonitors',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            'api_key': UPTIMEROBOT_API_KEY,
            'format': 'json',
            'logs': '0',
            'response_times': '0',
            'all_time_uptime_ratio': '1'
        },
        timeout=10
    )
    data = response.json()

    if data.get('stat') != 'ok':

        return jsonify({'status': 'error', 'message': 'Failed to fetch uptime'}), 500

    return jsonify({'status': 'success', 'monitors': data.get('monitors', [])})


###############################################
# PANEL ADMIN -> MODULES API
@admin_panel.route('/api/modules', methods=['GET', 'POST'])
@admin_required
def manage_modules():

    if request.method == 'POST':
    
        module_name = request.json.get('module')
        action = request.json.get('action')

    
    
        if module_name not in SERVER_MODULES:
    
            return jsonify({'status': 'error', 'message': 'Module not found'}), 404
        
    
    
        SERVER_MODULES[module_name]['enabled'] = (action == 'enable')


    
        # STOPPING SERVICESLOGIC 1    
        if action == 'disable' and SERVER_MODULES[module_name].get('thread'):

            SERVER_MODULES[module_name]['thread'].stop()
            SERVER_MODULES[module_name]['thread'] = None

        SERVER_MODULES[module_name]['enabled'] = (action == 'enable')





        # STARTING MODULES LOGIC 1
        if action == 'enable':

            try:
            
                thread = start_module(module_name, app=current_app)
                SERVER_MODULES[module_name]['thread'] = thread
            
            except Exception as e:
            
                return jsonify({'status': 'error', 'message': str(e)}), 500

        return jsonify({'status': 'success'})




    return jsonify({
        'modules': [
            {'name': name, 'enabled': data['enabled']} 
            for name, data in SERVER_MODULES.items()
        ]
    })




###############################################
# PANEL ADMIN -> SERVICES STUTAS API
@admin_panel.route('/api/services-status')
@admin_required
def services_status():
    
    try:
    
        from server.mainServices import service_manager
        return jsonify(service_manager.get_status())
    
    
    except Exception as e:
    
        current_app.logger.error(f"Error getting services status: {str(e)}")
    
        return jsonify({'status': 'error', 'message': str(e)}), 500



###############################################
# PANEL ADMIN -> SERVICES ON/OFF API

@admin_panel.route('/api/service-control', methods=['POST'])
@admin_required
def service_control():

    try:
    
        from server.mainServices import service_manager
    
        data = request.json
        service_name = data.get('service')
        action = data.get('action')  # 'start' o 'stop'
        
    
        if service_name not in service_manager.services:
    
            return jsonify({'status': 'error', 'message': 'Service not found'}), 404
        
        success = False
    
    
        if action == 'start':
            success = service_manager.start_service(service_name)
    
    
        elif action == 'stop':
            success = service_manager.stop_service(service_name)
    
    
        else:
    
            return jsonify({'status': 'error', 'message': 'Invalid action'}), 400
            
    
    
        return jsonify({
            'status': 'success' if success else 'error',
            'running': service_manager.services[service_name]['thread'] is not None
        })
        
    except Exception as e:
    
        current_app.logger.error(f"Error controlling service: {str(e)}")
    
        return jsonify({'status': 'error', 'message': str(e)}), 500

    



def start_admin(app):
    app.register_blueprint(admin_panel, url_prefix='/admin')