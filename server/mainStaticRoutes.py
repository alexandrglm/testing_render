from server.mainObjects import projects,allowed_root_files,static_pages
import os
import importlib
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO



def route_staticPages(app):

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
