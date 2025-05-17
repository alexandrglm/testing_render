from server.mainObjects import projects,allowed_root_files,static_pages
import os
import importlib
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO


def route_CSSJinja(app):

    @app.route('/templates/<project_id>/<filename>.css')
    def css_template(project_id, filename):

        css_path = f'{project_id}/{filename}.css.jinja'

        if not os.path.exists(os.path.join(app.template_folder, css_path)):

            return 'DEBUG (CSS Jinja/Back) Check CSS Jinja Routes', 404

        return render_template(css_path), 200, {'Content-Type': 'text/css'}
