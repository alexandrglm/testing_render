from server.mainObjects import projects,allowed_root_files,static_pages
import os
import importlib
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO



def route_alloweds(app):

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