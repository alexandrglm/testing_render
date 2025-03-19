############################################################################
# Project 10: WebShell project using websockets
#
#
################
from flask import Blueprint, render_template
from flask_socketio import emit
import subprocess
#############################
# Blueprint project10
project10 = Blueprint('project10', __name__)

@project10.socketio.on('exec_commander')
def commander(data):
    
    try:
        
        command = data.get('command', '')
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        output = result.stdout if result.returncode == 0 else result.stderr
        
        emit('commander_output', {'output': output})
    
    except Exception as e:
    
        emit('commander_output', {'output': f"Error - Commander exec error: {str(e)}"})
