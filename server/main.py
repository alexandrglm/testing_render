from server.mainObjects import projects,allowed_root_files,static_pages
import os
import importlib
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO
from markupsafe import Markup

def main_server(app):

    @app.route('/')
    def home():

        try: 
            
            return render_template('main.html', projects=projects)
        
        except Exception as e:

            print(f'DEBUG (Server/main route) -> ERROR / not rendering!!! : {str(e)}')
            return render_template('404/index_404.html')
