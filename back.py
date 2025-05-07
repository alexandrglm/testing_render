############################################################################
# STATIC PAGES
############################################################################
# Project:      Web Services demo back-end
# Date:         2025, May. 7th
############################################################################
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO
from markupsafe import Markup
import os
import re
import subprocess
import importlib
import requests
import time
import threading
from project10 import commander
from project12 import project12, socketio_opers
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

projects = [
    {'id': '14', 'title': 'React Deploys (1): Bottega\'s VSCode Analytics', 'desc': 'Bottega\'s React 14 web app for student VSCode analytics, adapted to React 18+ and served via Flask.'},
    {'id': '13', 'title': 'Studying Tools 2: Advanced Web Scraper       ', 'desc': 'URL-to-Markdown concept tool with custom CSS remapping (Custom DIVs, Bootstrap, components). MongoDB used as persistent storage.'},    
    {'id': '12', 'title': '(py)MongoDB Atlas WebShell                   ', 'desc': 'A MongoDb Atlas webshell for database manipulation using PyMongo (sync) and SocketIO in async mode.'},
    {'id': '11', 'title': '3D / VR Showcase test                        ', 'desc': 'First approach to developing VR/Augmented Reality environments.'},
    {'id': '10', 'title': 'WebShell                                     ', 'desc': 'Web-based interactive shell framework with real-time frontend-backend communication using Flask and Socket.IO'},
    {'id': '09', 'title': 'Studying Tools 1: MarkDown Web Server        ', 'desc': 'Parsing Markdown into HTML. A basic framework with auto-generated indexes for a documentation showroom.'},
    {'id': '08', 'title': 'Simple JSON DataBase Handler                 ', 'desc': 'An excuse to learn about dunders, @property decorators, Rest API GET/POST/PUT/PATCH/DETELE methods, and so on, and so forth.'},
    {'id': '07', 'title': '(Where) Is-ISS?                              ', 'desc': 'Yet another ISS live tracking tool using "requests" and JSON, but simplest.'},
    {'id': '06', 'title': 'Naiz Headlines, Now                          ', 'desc': 'Scraping headlines like if I were a junior devel. Best news and headlines scraping tool using Py. "requests" from naiz.eus.'},
    {'id': '05', 'title': 'InspectorView Demo                           ', 'desc': 'Why is this div not centered? Simple concept for a web CSS inspector tool.'},
    {'id': '04', 'title': 'App Test 02, but Logic performed at Back-End ', 'desc': 'App Test 02: AMSTRAD Color Tool converter using Python. Zero Front-end drama.'},
    {'id': '03', 'title': 'App Test 01, Logic performed via JS          ', 'desc': 'App Test 01: AMSTRAD Color Tool converter using JavaScript.'},
    {'id': '02', 'title': 'CSS Advanced Hello World                     ', 'desc': 'A less simpler HelloWorld screen CSS made with parallax effect and floating bubbles, fully over-hardcoded for no reason.'},
    {'id': '01', 'title': 'The Most Complex "Simple Hello World" site   ', 'desc': 'No frills, no HTML fuss—just Python.'},
    {'id': '404', 'title': 'Not Every Mistake is Truly a Mistake        ', 'desc': 'Sometimes, mistakes are masterpieces, unlike this error 404 page. '}
]

static_pages = [
    {'pathName' : 'about', 'link' : 'about/about.html'},
    {'pathName' : 'contact', 'link' : 'contact/contact.html'}
]

############################################################################
# Main web, projects logic
############################################################################
# main route
@app.route('/')
def home():

    return render_template('main.html', projects=projects)
#############
# Projects are integred as "modules"  by using Flask-Blueprint
for project in projects:
    
    project_id = project['id']
    module_name = f'project{project_id}'
    module_path = f'{module_name}.py'

    if os.path.exists(module_path):

        try:

            project_module = importlib.import_module(module_name)
            print(f'Project {project_id}: Module OK!')

            blueprint_name = f'project{project_id}'
            project_blueprint = getattr(project_module, blueprint_name)
            print(f'Project {project_id}: Blueprinted OK!')

            app.register_blueprint(project_blueprint, url_prefix=f'/{project_id}')
            print(f'Project {project_id} blueprint routes: OK!')

        except ImportError as e:

            print(f'ERROR: {project_id} loading errros found!: {e}')

        except AttributeError as e:

            print(f'ERROR: No {project_id} blueprints found!: {e}')

############################################################################
# When a project doesn't need its own .py, static routes for each project
@app.route('/<int:project_id>/')
def render_project(project_id):

    try:
        return render_template(f'{project_id}/index_{project_id}.html')

    except:

        print(f'ERROR: Can\'t render {project_id}!')
        return render_template('404/index_404.html')
############################################################################
# "If CSS Jinja is used" routes
@app.route('/templates/<project_id>/<filename>.css')
def css_template(project_id, filename):

    css_path = f'{project_id}/{filename}.css.jinja'

    if not os.path.exists(os.path.join(app.template_folder, css_path)):

        return 'DEBUG (CSS Jinja/Back) Check CSS Jinja Routes', 404

    return render_template(css_path), 200, {'Content-Type': 'text/css'}
############################################################################
# Static files routes
@app.route('/static/<path:filename>')
def static_files(filename):

    return send_from_directory('static', filename)
############################################################################
# STATIC PAGES
@app.route('/<path:pathName>/')
def render_statics(pathName):

    pathName = pathName.strip('/')

    page = next((p for p in static_pages if p['pathName'] == pathName), None)

    if page:

        try:
                        
            template_file = os.path.join(app.template_folder, page['link'])
            
            if not os.path.exists(template_file):
            
                print(f'DEBUG (Statics/Back) -> Check Static Pages logic - Dictionary : {template_file}')
                return render_template('404/index_404.html')
            
            return render_template(page['link'])
        
        
        except Exception as e:
            
            print(f'DEBUG (Static/Back) -> Error with {page} page : {str(e)}')
            
            return render_template('404/index_404.html')
    else:
        print('putadon')
        return render_template('404/index_404.html')


############################################################################
# CONTACT PAGE -> API, VALIDATIONS, SMTP
@app.route('/sendmail/', methods=['POST'])
def contact_email():

    try:

        # All validations (json, requireds, pass, configs), and then, exceptions, also resported in console/frontend
        if not request.is_json:
            print('DEBUG Contact -> Error Sending -> JSON error')
            return jsonify({'error': 'Content-Type must be application/json'}), 400

        mail_data = request.get_json()

        all_required_fields = ['name', 'email', 'message']

        if not all(field in mail_data for field in all_required_fields):

            return jsonify({'error': 'Missing required fields'}), 400

        smtp_password = os.getenv('SMTP_PASSWORD')
        if not smtp_password:
            print('DEBUG Contact -> .env error -> Password is missing')
            raise ValueError('DEBUG: SMTP config (pass) not set')
        

        smtp_config = {
            'server': os.getenv('SMTP_SERVER'),
            'port': int(os.getenv('SMTP_PORT')),
            'user': os.getenv('SMTP_USER'),
            'password': smtp_password.strip(),
            'account': os.getenv('SMTP_ACCOUNT', os.getenv('SMTP_USER'))
        }


        msg = MIMEText(
        f'''New message received from Contact form!

        -----------------------------------------
        From:    {mail_data['name'].strip()} - {mail_data['email'].strip()}
        Date: {datetime.now().strftime('%Y, %m. %d - %H:%M:%S')}
        -----------------------------------------

        - Message -
        {mail_data['message'].strip()}

        -----------------------------------------
        ''')
    
        msg['Subject'] = f'JustLearning CONTACT from -> {mail_data["name"]}'
        msg['From'] = smtp_config['user']
        msg['To'] = smtp_config['account']

        with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
            
            server.starttls()
            server.login(smtp_config['user'], smtp_config['password'])
            
            server.send_message(msg)

        return jsonify({'message': 'Message sent!'}), 200

    except ValueError as e:

        print(f'DEBUG (Contact) -> Config fail! (env?): {str(e)}')
        return jsonify({'error': str(e)}), 500
    
    except Exception as e:
    
        print(f'Unexpected error: {str(e)}')
        return jsonify({'error': 'Internal server error (is server on?)'}), 500
    

############################################################################
# Cookies management
@app.context_processor
def cookies_notice():

    def render_footer():
        return Markup(render_template('_footer.html'))

    return dict(render_footer = render_footer)
     
############################################################################
# SOCKETIO CONFIGS
socketio = SocketIO(
    app, cors_allowed_origins=[
        'http://127.0.0.1:8080',
        'https://127.0.0.1:8080',
        'http://localhost:8080',
        'https://localhost:8080',
        'http://0.0.0.0:8080',
        'https://0.0.0.0:8080',
        'http://127.0.0.1',
        'https://127.0.0.1',
        'https://justlearn.ing',
        'https://testing-render-zgdg.onrender.com'
    ], 
    monitor_clients=True, engineio_logger=True
)
############################################################################
# Projects callbacks for sockets io
#############
# Project 10: WebShell
socketio.on_event('exec_commander', commander)
#############
# Project 12: (py)MongoShell
os.environ['GEVENT_SUPPORT'] = 'True'
socketio_opers(socketio)

############################################################################
# REACT AUTO-DEPLOYMENTS
#############
# Project 14 React deploy script auto-start
def react_14_build():
    
    script_path = os.path.join(os.path.dirname(__file__), 'build.sh')
    
    if os.path.exists(script_path):
    
        try:
    
            print('DEBUG 14 -> Exec BUILD.SH')

            subprocess.run(['bash', script_path], check=True)
            
            print('DEBUG 14 - Build.sh OK!!!')
    
        except subprocess.CalledProcessError as e:
            
            print(f"DEBUG 14 -> ERROR EXEC BUILD.SH: {e}")
    
    else:
    
        print(f'DEBUG 14 -> BUILD.SH NOT FOUND!!! : {script_path}')

react_14_build()

############################################################################
# Flask keep-alive
################
def serverIP():

    print('Getting IP ...')

    while True:

        try:

            elKeep = requests.get('http://ipecho.net/plain')

            print(f'DEBUG -> Server IP is:  {elKeep.text}')

        except Exception as e:

            print(f'DEBUG -> Error getting IP : {e}')
            
        time.sleep(20)

############################################################################
# Flask init (Via SocketIo)
################
if __name__ == '__main__':

    threadIP = threading.Thread(target=serverIP, daemon=True)
    threadIP.start()
    
    socketio.run(app, host='0.0.0.0', port=8080, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)

