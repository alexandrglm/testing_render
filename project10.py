############################################################################
# Project 10: WebShell project using websockets
#
#
################
from flask import Blueprint, render_template, jsonify
from flask_socketio import emit
import subprocess
import os
#############################
# Blueprint project10
project10 = Blueprint('project10', __name__)

@project10.route('/')
def render_project_10():
    return render_template('10/index_10.html')

###################################################
# SECRETS to FRONT
@project10.route('/10/API_Secrets')
def handling_secrets():

    uri = os.environ.get('uri')

    return jsonify( { 'uri': uri } )