from server.mainObjects import projects,allowed_root_files,static_pages
import os
import importlib
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO



def routes_projects(app):
        
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