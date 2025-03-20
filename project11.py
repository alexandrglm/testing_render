############################################################################
# Project 11: WebXR framework
#
#
################
from flask import Flask, Blueprint, jsonify

project11 = Blueprint('project11', __name__)

@project11.route('/api/data')
def get_data():
    return jsonify({
        'model': 'monument_to_party_founding_dprk.glb', 
        'position': [0, -1.5, -5] 
    })