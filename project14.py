################################################################################
# Project 14: React Deployment using Flask (1):
# Concept:  Bottega's VSCode Analytics app deployed in Render -> Flask
################################################################################
from flask import Blueprint, render_template
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

project14 = Blueprint('project14', __name__)

BASE_DIR = Path('/opt/render/project/src') if 'RENDER' in os.environ else Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / 'static' / '14'
TEMPLATE_DIR = BASE_DIR / 'templates' / '14'

# This snippet (and callbacks) remains commented as long for debugging purposes, as ensuring assets is no longer needed in production.
# def ensure_assets():
#     js_path = STATIC_DIR / '14.js'
#     css_path = STATIC_DIR / '14.css'
#     if js_path.exists() and css_path.exists():
#         return True
#     print('DEBUG: Timeout error, server is still compiling React app\nPlease, reload again.')
#     return False


@project14.route('/')
def index():

    api_key = os.getenv('API_BOTTEGA')

    if not api_key:

        return 'DEBUG: API key error -> Please, set up your .env file including your own Bottega\'s API key as API_BOTTEGA = x', 500

    # This callback (and its function snippet) remains commented for debugging purposes,  as long as ensuring assets is no longer needed in production.
    # if not ensure_assets():
    #     return 'DEBUG: Error loading assets. Check server logs', 500
    
    return render_template('14/index_14.html', api_key=api_key)


@project14.route('/<path:subpath>')
def catch_all(subpath):

    return index()
