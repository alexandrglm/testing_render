############################################################################
# NUKEBOTS
#############
from flask import Flask, send_file, request, abort
import os
from server.sensitive_paths import SERVER_POISONED_PATHS

SERVER_BOT_KEYS = ['bot', 'spider', 'crawler', 'scraper', 'gpt', 'claude', 'google', 'bing', 'CCBot', 'CC']

SERVER_BOT_ALLOWED = os.getenv('SERVER_BOT_ALLOWED', '')

# SERVER_POISONED_PATHS was exported due to the extension

BOT_BOMB = 'static/server.map.xz'


def nuke_ram_bot(bot_ip, bot_user_agent, poisoned=False):

    nuked = '[NUKEBOT!]' if not poisoned else '[NUKEPATH!]' 

    print(f'\n[NUKEBOT!] -> New bot aimed: {bot_ip} - UserAgent: {bot_user_agent} ')

    if os.path.exists(BOT_BOMB):

        try:

            print(f'{nuked} -> Destroying payload sent!')
                  
            return send_file(
                BOT_BOMB,
                as_attachment=True,
                mimetype='application/x-xz',
                download_name='server.keys.xz'
            )
        
        except Exception as e:

            print(f'{nuked} ERROR -> Can\'nt send nukefile {BOT_BOMB}: {str(e)})')
            return abort(404, description='Server is down. Domain in sale.')
        
    else:
        
        print(f'{nuked} ERROR -> Undefined error, but bot went to void!')
        return abort(404, description='Server is down. Domain in sale.')

def serving_bots():

    bot_user_agent = request.headers.get('User-Agent').lower()
    bot_ip = request.remote_addr
    request_sensitive_path = request.path

    allowed_bots = [ allowed.strip() for allowed in SERVER_BOT_ALLOWED.split(',') if allowed.strip() ]
    
    # Inclussions

    if any( allowed.lower() in bot_user_agent for allowed in allowed_bots):

        return None
    
    # Exclussions

    if any( keyword.lower() in bot_user_agent for keyword in SERVER_BOT_KEYS):

        return nuke_ram_bot(bot_ip, bot_user_agent, poisoned=False)
    
    if request_sensitive_path in SERVER_POISONED_PATHS:

        return nuke_ram_bot(bot_ip, bot_user_agent, poisoned=True)
    

    return None







