############################################################################
# Project:      Web Services demo back-end
#
# FILE:        ./server/main.py STABLE
# BRANCH:        server-stable
#
# Date:         2025, May. 25th
############################################################################
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO
from markupsafe import Markup

import os
import time
import importlib
import threading
from dotenv import load_dotenv
import logging

from server.main import main_server, routes_projects, preCleanings
from server.mainObjects import projects, static_pages, allowed_root_files
# from server.mainProjects import routes_projects
from server.mainCSSJinja import route_CSSJinja
from server.mainStaticFiles import route_staticFiles
from server.mainStaticRoutes import route_staticPages
from server.mainRootAllowed import route_alloweds
from server.mainCookies import route_Cookies
from server.mainServices import service_manager
from server.mainBlog import start_blog

from serverModules.mail import start_server_email
# from serverModules.logs import start_server_logs
from serverModules.keep import start_server_keep
from serverModules.reacts import react_p14_build
from serverModules.nukebots import start_nukebots
from serverModules.telegram import telelog
from serverModules.paneldos import start_admin
from serverModules.panel_modules import start_module

from project10 import commander
from project12 import project12, socketio_opers

load_dotenv()

app = Flask(__name__)

############################################################################
# 0. SERVER STARTUP

preCleanings()

# #############
# # 0.0 Logs 
start_admin(app)
start_module(app)
# #############
# # 0.2 Logs 
# start_server_logs(app)

# #############
# # 0.1 NukeBots
start_nukebots(app)

# #############
# # 0.4 Telegram
telelog.init_app(app)

# #############
# # 0.3 SMTP
start_server_email(app)
            
#############
# 1. MAIN ROUTES
main_server(app)

#############
# 2. PROJECTS ROUTES
routes_projects(app)    


#############
# 3. CSS.jinja ROUTES
route_CSSJinja(app)
#############
# 4. STATIC FILES
route_staticFiles(app)
#############
# 5. STATIC PAGES
route_staticPages(app)
# #############
# 6. ALLOWED STATIC FILES ON /
route_alloweds(app)
#############
# 7. COOKIES 
route_Cookies(app)

#############
# 7. COOKIES 
start_blog(app)


############################################################################
# 8. SOCKETIO/Flask - CORS CONFIGS

SERVER_CORS = os.getenv('SERVER_CORS')
SERVED_CORS = [ origin.strip() for origin in SERVER_CORS.split(',') if origin.strip() ]

socketio = SocketIO(
    app, cors_allowed_origins=SERVED_CORS,
    monitor_clients=True, engineio_logger=True
)


############################################################################
# 9. REACT - PROJECT CALLBACKS

# #############
# # Project 14 (React)
react_p14_build()


#############
# Project 12: (py)MongoShell (via its own socketio def)
os.environ['GEVENT_SUPPORT'] = 'True'

# #############
# # Project 10: WebShell (via Socketio)
socketio.on_event('exec_commander', commander)
socketio_opers(socketio)


############################################################################
# 10. Flask init + Last callbacks
################
if __name__ == '__main__':

    # GETTIN SERVICES FROM mainServices
    service_manager.register_services(app)

    # # STARTING SPECIAL SERVICES
    service_manager.start_service('telegram')
    time.sleep(2)


    # # STARTING REGULAR SERVICES -> Pending iterate from over services lists ...
    for service_name in [
        # 'logs',
        'mail',
        'nukebots',
        'keep'
        ]:

        service_manager.start_service(service_name)
    
    
    
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
        
        print('\nCleanStopping serices ...\n')

    #     telelog.stop()

        for service_name in service_manager.services:

            service_manager.stop_service(service_name)
    
    
    
    except Exception as e:
        app.logger.error(f'[DEBUG] -> Unexpected server error! : {str(e)}')
    
    
    finally:

        print('\nServer stopped. Bye!!')
