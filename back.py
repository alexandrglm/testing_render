############################################################################
# Project:      Web Services demo back-end
# Date:         2025, March. 12th
############################################################################
from flask import Flask, render_template, send_from_directory
import os
import importlib

app = Flask(__name__)


projects = [
    {'id': '01', 'title': 'The Most Complex "Simple Hello World" site', 'desc': 'No frills, no HTML fuss—just Python.'},
    {'id': '02', 'title': 'CSS Advanced Hello World', 'desc': 'A less simpler HelloWorld screen made by CSS with parallax effect and floating bubbles, fully over-hardcoded for no reason.'},
    {'id': '03', 'title': 'Back-End only as server', 'desc': 'App Test 01: AMSTRAD Color Tool converter using JavaScript.'},
    {'id': '04', 'title': 'Back-End as Logic', 'desc': 'App Test 02: AMSTRAD Color Tool converter using Python. Zero Front-end drama.'},
    {'id': '05', 'title': 'InspectorView Demo', 'desc': 'Why is this div not centered? Simple concept for a web CSS inspector tool.'},
    {'id': '06', 'title': 'Naiz Headlines, Now', 'desc': 'Scraping headlines like if I were a junior devel. Best news and headlines scraping tool using Py. "requests" from naiz.eus.'},
    {'id': '07', 'title': '(Where) Is-ISS?', 'desc': 'Yet another ISS live tracking tool using "requests" and JSON, but simplest.'},
    {'id': '08', 'title': 'Profile Info Getter/Setter', 'desc': 'An excuse to learn about __init_, __main__, @property decorators and so on, and so forth, by serving a fully "Profiles/Records" framework.'},
    {'id': '09', 'title': 'Study Framework 1: MarkDown Web Server', 'desc': 'Parsing Markdown into HTML. A basic framework with auto-generated indexes for a documentation showroom.'},
    {'id': '404', 'title': 'Not Every Mistake is Truly a Mistake', 'desc': 'Sometimes, mistakes are masterpieces, unlike this error 404 page. '}
]

############################################################################
# Main web, projects logic
############################################################################
# main route
@app.route('/')
def home():
    return render_template('main.html', projects=projects)
############################################################################
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
            print(f'Project {project_id} blueprint router: OK!')
        
        except ImportError as e:

            print(f'ERROR: {project_id} loading errros found!: {e}')
        
        except AttributeError as e:

            print(f'ERROR: No {project_id} blueprints found!: {e}')

############################################################################
# When a project doesn't need its own .py, static routes for each project
@app.route('/<project_id>/')
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
        
        return "Not found, use static/<project_id> route", 404
    
    return render_template(css_path), 200, {'Content-Type': 'text/css'}
############################################################################
# Static files routes
@app.route('/static/<path:filename>')
def static_files(filename):

    return send_from_directory('static', filename)
############################################################################

# server init, 0.0.0.0 required for Render, deact. debug before committing
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)