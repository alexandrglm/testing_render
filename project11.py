############################################################################
# Project 11: WebXR framework
#
#
################
from flask import Flask, Blueprint, jsonify, send_from_directory
import os

project11 = Blueprint('project11', __name__)

# Pendiente para posible muestrario de escenas
# @project11.route('/shaders')
# def get_shaders():
#     shader_path = os.path.join(current_app.static_folder, '11/shaders')
    
#     return send_from_directory(shader_path, 'shader.frag')

@project11.route('/api/data')
def get_data():
    return jsonify({
        'model': 'monument_to_party_founding_dprk.glb', 
        'position': [0, 0, 0] 
    })