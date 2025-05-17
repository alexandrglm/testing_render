from server.mainObjects import projects,allowed_root_files,static_pages
import os
import importlib
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO


def route_staticFiles(app):

    @app.route('/static/<path:filename>')
    def static_files(staticFilename):

        try:

            return send_from_directory('static', staticFilename)

        except Exception as e:

            print(f'DEBUG (Server/Statics files) -> Static FILE or PATH error : {str(e)}')
            return render_template('404/index_404.html')