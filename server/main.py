from server.mainObjects import projects,allowed_root_files,static_pages
import os
import importlib
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO
from markupsafe import Markup

# FILE:        ./server/main.py STABLE
# BRANCH:        server-stable
"""
# #########################
#   MAIN ROUTES (server-stable branch)
#   
#   Changes from old:
#
#       - projects -> combined_content (projects + blog)
#       - 
#       - Minding for New Objects' Value - Keys (Date, Type, Order)
        - 
        - Add rendering_checks (Objects -> Projects -> Mandarory fields)
        - Add combined_content func ->Handler, Get and mix projects+blogs as intended
        -
        - Add main_blog_funcs (routes for self 'snapshots'). Might be exported to a new mainBlog.py logic snippet.
        -
"""
def main_server(app):
    @app.route('/')
    def home():
        
        try:
            combined_content = main_combineds()
            return render_template('main.html', combined_content=combined_content)
        
        except Exception as e:

            print(f'[ERROR] (Server/main route) -> Main / failed! : {str(e)}')
            return render_template('404/index_404.html')
        
    
    def main_combineds(): # pending -> Class plus constructors???

        not_hidden = [p for p in projects if not p.get('hidden', False)]
        
        not_hidden.sort(key=lambda x: int(x.get('order', '999')))
        
        return not_hidden





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



    def main_blog_snapshot(project):

        metadata = project.get('metadata', {})
        if metadata.get('snapshot'):
            
            date_splits = metadata.get('date', '').split('-')
            
            # Date -> Length valids
            if len(date_splits) >= 2:

                year, month = date_splits[0], date_splits[1]
                
                link = metadata.get('link', 'default')
                
                filename = f"blog/{year}/{month}/{link}/{metadata['snapshot']}"
                return send_from_directory('static', filename)
        
        # add log '[WARN]') or smething
        return send_from_directory('static', 'blog-default-cardboard.png')
        



# Pending -> Might be a class bor main/projects/blogs??????
def rendering_checks():

    for i, project in enumerate(projects):
        """
        MANDATORIES:
            - Order     -> For JinjaRendering order    
            - Type      -> 'project', 'blog', etc
            - Size      -> Cardboards' rendering sizes (default, double, mino)
            - Hidden    -> bool

            If Type == 'project':
                - id

            If Type == 'Blog:
                - Metadata -> Link  : 
                - Metadata -> Date
                - Metadata -> Title
        """
        # PENDING -> If Duplicated ORDER
        
        # FOR Projects+blogs SHARED MANDATORIES
        if not project.get('order'):
            print(f'\n[ERROR] (OBJECTS) -> "{i}" HAS NO "ORDER"\n\n')
        
        if not project.get('type'):
            print(f'\n[ERROR] (OBJECTS) -> "{i}" HAS NO "TYPE"\n\n')
        
        if not project.get('size'):
            print(f'\n[ERROR] (OBJECTS) -> "{i}" HAS NO "SIZE"\n\n')
        
        if 'hidden' not in project:
            print(f'\n[ERROR] (OBJECTS) -> "{i}" HAS NO "HIDDEN"\n\n')

        
        # FOR Projetc MANDATORIES (ID's)
        if project.get('type') == 'project' and not project.get('id'):
            print(f'\n[ERROR] (OBJECTS) -> "{i}" is "PROJECT" but HAS NO "ID"\n\n')
        
        
        # FOR Blog MANDATORIES (date, link)
        if project.get('type') == 'blog':

            metadata = project.get('metadata', {})
            
            if not metadata.get('link'):
                print(f'\n[ERROR] (OBJECTS) -> "{i}" is "BLOG" but HAS NO "LINK"\n\n')
            
            if not metadata.get('date'):
                print(f'\n[ERROR] (OBJECTS) -> "{i}" is "BLOG" but HAS NO "DATE"\n\n')
        
        # FOR ALL VALIDS
        if not project.get('metadata', {}).get('title'):
            print(f'\n[ERROR] (OBJECTS) -> "{i}" HAS NO "TITLE"\n\n')


rendering_checks()
