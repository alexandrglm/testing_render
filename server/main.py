from server.mainObjects import blogs,projects,allowed_root_files,static_pages
import os
import importlib
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO
from markupsafe import Markup

# FILE:        ./server/main.py STABLE
# BRANCH:        server-stable

# #########################
#   MAIN ROUTES (server-stable branch)
#   
#   Changes from old:
#
#       - projects -> combined_content (projects + blog)
#       - 
#       - Minded for New Objects' Value - Keys (Date, Type, Order)


def main_server(app):
    @app.route('/')
    def home():
        
        try:
            combined_content = get_combined_content()
            return render_template('main.html', combined_content=combined_content)
        
        except Exception as e:

            print(f'[ERROR] (Server/main route) -> Main / failed! : {str(e)}')
            return render_template('404/index_404.html')


def routes_projects(app):
    
    # ./project/<id>/<id>.py
    project_items = [p for p in projects if p.get('type') == 'project' and p.get('id')]
    
    for project in project_items:
        
        project_id = project['id']
        module_name = f'project{project_id}'
        module_path = f'{module_name}.py'
    

        if os.path.exists(module_path):
            
            try:
            
                project_module = importlib.import_module(module_name)
                print(f'Project {project_id} -> Exists!')
            
                blueprint_name = f'project{project_id}'
                project_blueprint = getattr(project_module, blueprint_name)
                print(f'Project {project_id} -> Blueprint loaded!')
                    
                app.register_blueprint(project_blueprint, url_prefix=f'/project/{project_id}')
                print(f'Project {project_id} -> Loaded! [OK!]')
            
            except ImportError as e:

                print(f'\n[ERROR] -> {project_id} LOADING errors: \n   {str(e)} \n\n')
            
            
            except AttributeError as e:
                
                print(f'\n[ERROR] -> {project_id} LOGIC errors: \n   {str(e)} \n\n')
    


    @app.route('/project/<project_id>/')
    def render_project(project_id):
        
        try:
            return render_template(f'{project_id}/index_{project_id}.html')
        
        except Exception as e:
            
            print(f'\n[ERROR] (Projects) -> {project_id} RENDERING errors :\n   {str(e)}\n\n')
            return render_template('404/index_404.html')




###############
# Posts 
def routes_blogs(app):

    @app.route('/blog/<int:year>/<int:month>/<slug>/')
    def render_blog(year, month, slug):
        
        
        # metadata.link + metadata.YYYY--metadata-MM
        blog = next((p for p in projects 
                    if p.get('type') == 'blog' 
                    and p.get('metadata', {}).get('link') == slug
                    and p.get('metadata', {}).get('date', '').startswith(f'{year}-{month:02d}')), None)
        
        # Pending checks, might be duplicated as Exception does
        if not blog:

            return render_template('404/index_404.html')
        
        
        try:
            
            template_path = f'blog/{year}/{month:02d}/{slug}/{slug}.html'
            return render_template(template_path, blog=blog)
        
        except Exception as e:
            
            print(f'\n[ERROR] (BLOGS) -> {template_path} error :\n   {str(e)}\n\n')
            return render_template('404/index_404.html')
