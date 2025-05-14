############################################################################
# Project:      Web Services demo back-end
# Date:         2025, May. 14th
############################################################################
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO
from markupsafe import Markup
import os
import time
import importlib
import threading
from project10 import commander
from project12 import project12, socketio_opers
from dotenv import load_dotenv
from server.mail import start_server_email
from server.logs import start_server_logs
from server.keep import start_server_keep
from server.reacts import react_p14_build
from server.nukebots import start_nukebots
from server.telegram import telelog
from server.panel import start_admin

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

allowed_root_files = [
    {'filename' : 'robots.txt'},
    {'filename' : 'version.txt'}
]


############################################################################
# 0. SERVER STARTUP
#############


#############
# 0.0 Logs 
start_admin(app)

#############
# 0.2 Logs 
start_server_logs(app)

#############
# 0.1 NukeBots
start_nukebots(app)

#############
# 0.4 Telegram
telelog.init_app(app)

#############
# 0.3 SMTP
start_server_email(app)
            
############################################################################
# 1. MAIN ROUTES
@app.route('/')
def home():

    try: 
        
        return render_template('main.html', projects=projects)
    
    except Exception as e:

        print(f'DEBUG (Server/main route) -> ERROR / not rendering!!! : {str(e)}')
        return render_template('404/index_404.html')


############################################################################
# 2. PROJECTS ROUTES
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

            app.register_blueprint(project_blueprint, url_prefix=f'/project/{project_id}')
            print(f'Project {project_id} blueprint routes: OK!')

        except ImportError as e:

            print(f'ERROR: {project_id} loading errros found!: {str(e)}')

        except AttributeError as e:

            print(f'ERROR: No {project_id} blueprints found!: {str(e)}')


@app.route('/project/<project_id>/')
def render_project(project_id):

    try:
    
        return render_template(f'{project_id}/index_{project_id}.html')

    except Exception as e:

        print(f'DEBUG (Projects) Can\'t render {project_id}! :  {str(e)}')
        return render_template('404/index_404.html')
    
############################################################################
# 3. CSS.jinja ROUTES
@app.route('/templates/<project_id>/<filename>.css')
def css_template(project_id, filename):

    css_path = f'{project_id}/{filename}.css.jinja'

    if not os.path.exists(os.path.join(app.template_folder, css_path)):

        return 'DEBUG (CSS Jinja/Back) Check CSS Jinja Routes', 404

    return render_template(css_path), 200, {'Content-Type': 'text/css'}

############################################################################
# 4. STATIC FILES
@app.route('/static/<path:filename>')
def static_files(staticFilename):

    try:

        return send_from_directory('static', staticFilename)

    except Exception as e:

        print(f'DEBUG (Server/Statics files) -> Static FILE or PATH error : {str(e)}')
        return render_template('404/index_404.html')

############################################################################
# 5. STATIC PAGES
@app.route('/<path:pathName>/')
def render_statics(pathName):

    pathName = pathName.strip('/')

    page = next((p for p in static_pages if p['pathName'] == pathName), None)

    if pathName.startswith('project/') or pathName == 'static':

        return render_template('404/index_404.html')


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
    
        print(f'DEBUG (Static/Back) -> UNDEFINED ERROR ')
        return render_template('404/index_404.html')


# ############################################################################
# 6. ALLOWED STATIC FILES ON /
@app.route('/<filename>')
def root_statics(filename):

    allowed_files =  [ file['filename'] for file in allowed_root_files  ]

    if filename in allowed_files:
    
        filepath = os.path.join('.', filename)
    
        if os.path.exists(filepath):
    
            try:
                
                return send_from_directory('.', filename)
    
            except Exception as e:
   
                print(f'DEBUG (Statics on /) -> Error serving {filename}: {str(e)}')
    
        else:
   
            print(f'DEBUG (Statics on /) -> {filename} allowed NOT FOUND on /!')

    else:
    
        print(f'DEBUG (Statics on /) -> {filename} is NOT allowed for /!')

    return render_template('404/index_404.html')

############################################################################
# 7. COOKIES 
@app.context_processor
def cookies_notice():

    def render_footer():
        return Markup(render_template('_footer.html'))

    return dict(render_footer = render_footer)


###########################################################################
# 8. SOCKETIO/Flask - CORS CONFIGS
SERVER_CORS = os.getenv('SERVER_CORS')

socketio = SocketIO(
    app, cors_allowed_origins=[ origin.strip() for origin in SERVER_CORS.split(',') if origin.strip() ],
    monitor_clients=True, engineio_logger=True
)

############################################################################
# 9. REACT - PROJECT CALLBACKS
#############
# Project 14 (React)
react_p14_build()
#############
# Project 12: (py)MongoShell (via its own socketio def)
os.environ['GEVENT_SUPPORT'] = 'True'
#############
# Project 10: WebShell (via Socketio)
socketio.on_event('exec_commander', commander)
socketio_opers(socketio)


############################################################################
# 10. Flask init + Last callbacks
################
if __name__ == '__main__':

    services = {
        'keep': threading.Thread(target=start_server_keep, daemon=True),
        'telegram': threading.Thread(target=telelog.start_polling, daemon=True),
        'logs': threading.Thread(target=lambda: start_server_logs(app), daemon=True)
    }


    services['telegram'].start()
    time.sleep(2) 

    for name, service in services.items():
        
        if name != 'telegram':
            service.start()

    
    try:
        
        print('DEBUG [All] -> Starting server ...')
        
        socketio.run(
            app, 
            host='0.0.0.0', 
            port=8080, 
            debug=True, 
            use_reloader=False,
            allow_unsafe_werkzeug=True
        )

    except KeyboardInterrupt:
        
        print('\nStopping modules safely ...\n')
        telelog.stop()
    
    except Exception as e:

        app.logger.error(f'Error fatal: {str(e)}')
    
    finally:
        print('\nServer stopped!')