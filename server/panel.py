############################################################################
# ADMIN
from flask import Flask, render_template, send_from_directory, request, jsonify, abort
import socket
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import json

# ADMIN_PASS = os.getenv('ADMIN_HASH')

# def admin_pass_hash(input_pass):

#     return hmac.compare_digest(input_pass, ADMIN_PASS)

# @app.route('/admin/auth')
# def get_auth():

#     if not admin_pass_hash(request.headers.get('X-Admin-Token')):

#         abort(403) # mas adelante pensar usarun 403.html

#     with open('/etc/secrets/admin.json') as f:

#         return jsonify(json.load(f))

# app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
# jwt = JWTManager(app)

# ADMIN_PASSWORD_HASH = generate_password_hash(os.getenv('ADMIN_PASSWORD'))



# @app.route('/admin/login', method=['POST'])
# def admin_auth():

#     if not request.is_json:

#         return jsonify({'error': 'DEBUG (Admin Routes) -> JSON is missing'}), 400
    
#     password = request.json.get('password', None)

#     if not password:

#         return jsonify({'error': 'DEBUG (Admin Routes) -> PASSWORD is missing'}), 400

#     if check_password_hash(ADMIN_PASSWORD_HASH, password):

#         access_token = create_access_token(identity='admin') 
    
#         return jsonify(access_token=access_token), 200


#     return jsonify({'error': 'DEBUG (admin) -> Bad password hash checking'})
    
# @app.route('/admin/secrets/<filename>', methods=['GET'])
# @jwt_required()

# def get_secret_file(filename):

#     try:

#         if get_jwt_identity() != 'admin':

#             return jsonify({'error': 'DEBUG (Secrets) -> You are not an admin!'}), 403


#         if not filename.endswith(('.json', '.html', '.txt', '.log')):
            
#             return jsonify({'error': 'DEBUG (Secrets) -> Filetype NOT allowed!'}), 400

#         secret_path = os.path.join('/etc/secrets', filename)
        
#         if not os.path.exists(secret_path):

#             return jsonify({'error': 'DEBUG (Secrets) -> File not found in secrets!'}), 404


#         with open(secret_path, 'r') as f:

#             if filename.endswith('.json'):
            
#                 return jsonify(json.load(f))
            
#             else:
            
#                 return f.read(), 200, {'Content-Type': 'text/plain'}

    
#     except Exception as e:
        
#         return jsonify({'error': f'DEBUG (Secrets) Internal server error -> {str(e)}'}), 500

# Queda pendiente:
# 1. Generar rutas siempre protegidas copn este formato:





