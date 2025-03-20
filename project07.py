############################################################################
# Project 07: A basic tracker tool using coordiantes provided in a json
################
# Imports: 
from flask import Blueprint, Flask, render_template, jsonify
import requests
############################################################################
# 07 Logic
#################
# app.route to blueprint
project07 = Blueprint('project07', __name__)
##################
@project07.route('/07/')
def render_project_07():
    return render_template('07/index_07.html')

@project07.route('/iss_position')

def iss_position():
    
    try:
        url = 'http://api.open-notify.org/iss-now.json'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        longitude = data['iss_position']['longitude']
        latitude = data['iss_position']['latitude']

        return jsonify({'longitude': longitude, 'latitude': latitude})
    
    except requests.RequestException as e:
        return jsonify({'error': f"Failed to get ISS position: {e}"}), 500

