############################################################################
# NUKEBOTS
#############
from flask import send_file, request, abort
import os
import re
from serverModules.sensitive_paths import SERVER_POISONED_PATHS, sensitive_match
from dotenv import load_dotenv

load_dotenv()

SERVER_BOT_KEYS = ['bot', 'spider', 'crawler', 'scrap', 'gpt', 'claude', 'google', 'bing', 'CC']
SERVER_BOT_ALLOWED = [b.strip().lower() for b in os.getenv('SERVER_BOT_ALLOWED', '').split(',') if b.strip()]
BOT_BOMB = 'static/server.map.xz'

def contains_keyword(text, keywords):

    text = text.lower()
    return any(re.search(rf'\b{re.escape(k.lower())}\b', text) for k in keywords)

def nuke_ram_bot(bot_ip, bot_user_agent, poisoned=False):
    
    nuked = '[NUKEPATH!]' if poisoned else '[NUKEBOT!]'
    print(f'\n{nuked} -> Target: {bot_ip} | UserAgent: {bot_user_agent}')

    
    if os.path.exists(BOT_BOMB):
    
        try:
    
            return send_file(
                BOT_BOMB,
                as_attachment=True,
                mimetype='application/x-xz',
                download_name='server.keys.xz'
            )
    
        except Exception as e:
    
            print(f'{nuked} ERROR -> Failed to send payload: {str(e)}')
    
    else:
    
        print(f'{nuked} ERROR -> Payload file not found!')


    return abort(404, description='Server is down. Domain in sale.')

def serving_bots():

    path = request.path
    user_agent = request.headers.get('User-Agent', '').lower()
    host = request.host.lower()
    ip = request.remote_addr

    """
    1 -> EXCLUSSION

    2 -> ALLOW SERVER_BOT_ALLOWED
    3 -> DENY HOST KEYWORDS
    4 -> DENY UA KEYWORDS

    5 -> ALLOW ELSEWERE
    """
    if sensitive_match(path):
    
        return nuke_ram_bot(ip, user_agent, poisoned=True)


    if any(allowed in user_agent for allowed in SERVER_BOT_ALLOWED):
    
        return None

    if contains_keyword(host, SERVER_BOT_KEYS):
    
        return nuke_ram_bot(ip, f'Host: {host} | UA: {user_agent}', poisoned=False)
    
    
    if contains_keyword(user_agent, SERVER_BOT_KEYS):
    
        return nuke_ram_bot(ip, user_agent, poisoned=False)

    
    return None

def start_nukebots(app):
    
    @app.before_request
    def filtering_bots():
    
        bot_detected = serving_bots()
    
        if bot_detected:
    
            return bot_detected
