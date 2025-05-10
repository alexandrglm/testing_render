############################################################################
# NUKEBOTS
#############
from flask import Flask, send_file, request, abort
import os


SERVER_BOT_KEYS = ['bot', 'spider', 'crawler', 'scraper', 'gpt', 'claude', 'google', 'bing', 'CCBot', 'CC']

SERVER_BOT_ALLOWED = os.getenv('SERVER_BOT_ALLOWED', '')

BOT_BOMB = 'static/server.map.xz'

def serving_bots():


    bot_user_agent = request.headers.get('User-Agent').lower()
    bot_ip = request.remote_addr

    allowed_bots = [ allowed.strip() for allowed in SERVER_BOT_ALLOWED.split(',') if allowed.strip() ]

    if any( allowed.lower() in bot_user_agent for allowed in allowed_bots):

        return None
    
    if any( keyword.lower() in bot_user_agent for keyword in SERVER_BOT_KEYS ):

        print(f'\n[NUKEBOT!!!] -> New bot aimed: {bot_ip} - UserAgent: {bot_user_agent} ')

        if os.path.exists(BOT_BOMB):

            try:
        
                print('[NUKEBOT!!!] -> New RAM\'s Bot fed with tons of trash GB :-D')
                return send_file(BOT_BOMB, as_attachment=True, mimetype='application/x-xz', download_name='server.map.xz')

            
            except Exception as e:
        
                print('[NUKEBOT Error] -> Can\'nt send nukefile {BOT_BOMB}: {str(e)})')
                return abort(404, description='Server is down. Domain in sale.')
        
        else:

            print('[NUKEBOT ERROR] -> Bot was redirected to None')
            return abort(404, description='Server is down. Domain in sale.')

    return None

