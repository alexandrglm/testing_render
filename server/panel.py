############################################################################
# ADMIN PANEL - VERSION FINAL CORREGIDA
############################################################################
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import os
import time
from flask import Flask, abort, render_template, render_template_string, send_from_directory, request, jsonify, redirect, url_for
import requests
from dotenv import load_dotenv
from functools import wraps
import psutil

load_dotenv()

ADMIN_SECRETS = os.getenv('ADMIN_SECRETS')
ADMIN_HASH = os.getenv('ADMIN_HASH')
ADMIN_SESSION_TIMEOUT = int(os.getenv('ADMIN_SESSION_TIMEOUT', '1800'))  # 30 min

ADMIN_SESSION = {
    'is_admin': False,
    'last_activity': None,
    'timeout': ADMIN_SESSION_TIMEOUT
}

def start_admin(app):
    def get_secure_template(template_name):
        try:
            template_path = os.path.join(ADMIN_SECRETS, template_name)
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            app.logger.error(f'Error loading template {template_name}: {str(e)}')
            return None

    def validate_admin_session():
        if ADMIN_SESSION['is_admin']:
            now = datetime.now()
            last_activity = ADMIN_SESSION['last_activity']

            if last_activity and (now - last_activity).total_seconds() > ADMIN_SESSION['timeout']:
                ADMIN_SESSION['is_admin'] = False
                return False

            ADMIN_SESSION['last_activity'] = now
        return ADMIN_SESSION['is_admin']

    def admin_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not validate_admin_session():
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'error': 'Admin access required'}), 403
                abort(403, description="Admin access required")
            return func(*args, **kwargs)
        return wrapper

    # API Routes
    @app.route('/admin/api/check-auth')
    def check_admin_auth():
        return jsonify({
            'is_admin': validate_admin_session(),
            'timeout': ADMIN_SESSION_TIMEOUT - (datetime.now() - ADMIN_SESSION['last_activity']).total_seconds()
                        if ADMIN_SESSION['last_activity'] else 0
        })

    @app.route('/admin/api/system-stats')
    @admin_required
    def system_stats():
        try:
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
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/admin/api/secrets-list')
    @admin_required
    def secrets_list():
        try:
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
            
            return jsonify({
                'status': 'success',
                'secrets': secrets
            })
        except Exception as e:
            app.logger.error(f'Error listing secrets: {str(e)}')
            return jsonify({
                'status': 'error',
                'message': 'Error al listar archivos'
            }), 500

    def format_file_size(size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} GB"

    @app.route('/admin/api/secrets/<filename>')
    @admin_required
    def admin_secret_content(filename):
        try:
            if not filename or '..' in filename or filename.startswith('/'):
                raise ValueError('Invalid filename')
            
            secret_path = os.path.join(ADMIN_SECRETS, filename)
            if not os.path.isfile(secret_path):
                raise FileNotFoundError('File not found')
                
            return send_from_directory(
                ADMIN_SECRETS, 
                filename, 
                as_attachment=False,
                mimetype='text/plain'
            )
        except Exception as e:
            app.logger.error(f'Secret access error: {str(e)}')
            return jsonify({
                'status': 'error',
                'message': 'Failed to access secret file'
            }), 404

    @app.route('/admin/api/module/<module_name>')
    @admin_required
    def get_admin_module(module_name):
        valid_modules = ['dashboard_module.html', 'stats_module.html', 'secrets_module.html']
        if module_name not in valid_modules:
            abort(404)
        
        module_content = get_secure_template(module_name)
        if not module_content:
            abort(404)
        
        return module_content

    @app.route('/admin/api/uptime-stats')
    @admin_required
    def uptime_robot_stats():
        try:
            api_key = os.getenv("UPTIMEROBOT_API_KEY")
            if not api_key:
                return jsonify({
                    'status': 'error',
                    'message': 'UptimeRobot API key not configured'
                }), 500

            response = requests.post(
                'https://api.uptimerobot.com/v2/getMonitors',
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Cache-Control': 'no-cache'
                },
                data={
                    'api_key': api_key,
                    'format': 'json',
                    'logs': '0',
                    'response_times': '0',
                    'all_time_uptime_ratio': '1'
                },
                timeout=10
            )
            
            data = response.json()
            if data.get('stat') != 'ok':
                raise Exception(data.get('error', {}).get('message', 'Unknown error'))

            return jsonify({
                'status': 'success',
                'monitors': data.get('monitors', [])
            })
        except Exception as e:
            app.logger.error(f'UptimeRobot error: {str(e)}')
            return jsonify({
                'status': 'error',
                'message': 'Failed to fetch uptime data'
            }), 500

    # Admin Panel Routes
    @app.route('/admin')
    def admin_root():
        if validate_admin_session():
            return redirect(url_for('admin_panel'))
        return redirect(url_for('admin_login'))

    @app.route('/admin/login', methods=['GET'])
    def admin_login():
        if validate_admin_session():
            return redirect(url_for('admin_panel'))
        return render_template('admin/login.html')

    @app.route('/admin/login', methods=['POST'])
    def admin_login_submit():
        password = request.form.get('password')
        if not password or not check_password_hash(ADMIN_HASH, password):
            return jsonify({'error': 'Invalid credentials'}), 401

        ADMIN_SESSION.update({
            'is_admin': True,
            'last_activity': datetime.now()
        })
        return jsonify({'redirect': url_for('admin_panel'), 'status': 'success'})

    @app.route('/admin/panel')
    @admin_required
    def admin_panel():
        modules = {
            'dashboard': get_secure_template('dashboard_module.html') or '<div class="error">Failed to load dashboard</div>',
            'stats': get_secure_template('stats_module.html') or '<div class="error">Failed to load stats</div>',
            'secrets': get_secure_template('secrets_module.html') or '<div class="error">Failed to load secrets</div>'
        }
        
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Panel</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            {{ dashboard|safe }}
            {{ stats|safe }}
            {{ secrets|safe }}
        </body>
        </html>
        """, **modules)

    @app.route('/admin/logout')
    def admin_logout():
        ADMIN_SESSION.update({
            'is_admin': False,
            'last_activity': None
        })
        return redirect(url_for('admin_login'))

    # Security Middleware
    @app.before_request
    @app.before_request
    def admin_security_middleware():
        if request.path.startswith('/admin'):
            allowed_routes = ['admin_login', 'admin_login_submit', 'static']
            
            if request.endpoint not in allowed_routes:
                if not validate_admin_session():
                    if request.path.startswith('/admin/api'):
                        return jsonify({
                            'status': 'error',
                            'message': 'Session expired'
                        }), 403
                    return redirect(url_for('admin_login'))

    # Disable caching for admin routes
    @app.after_request
    def disable_caching(response):
        if request.path.startswith('/admin'):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'
        return response

    # Error handlers
    @app.errorhandler(403)
    def forbidden(e):
        if request.path.startswith('/admin/api'):
            return jsonify({'status': 'error', 'message': 'Forbidden'}), 403
        return redirect(url_for('admin_login'))

    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith('/admin'):
            return redirect(url_for('admin_login'))
        return e

    # Verify all critical routes are registered
    if os.getenv('FLASK_ENV') == 'development':
        def verify_protected_routes():
            required_routes = {
                '/admin/api/system-stats': 'system_stats',
                '/admin/api/secrets-list': 'secrets_list',
                '/admin/api/module/dashboard_module.html': 'get_admin_module',
                '/admin/panel': 'admin_panel'
            }
            
            registered_routes = {str(rule): rule.endpoint for rule in app.url_map.iter_rules()}
            
            for route, endpoint in required_routes.items():
                if not any(r.startswith(route) for r in registered_routes):
                    raise AssertionError(f"Route {route} not properly registered")
            
            print("✓ All critical routes are properly registered")
        
        verify_protected_routes()