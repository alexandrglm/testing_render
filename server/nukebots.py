############################################################################
# NUKEBOTS
#############
from flask import Flask, send_file, request, abort
import os


SERVER_BOT_KEYS = ['bot', 'spider', 'crawler', 'scraper', 'gpt', 'claude', 'google', 'bing', 'CCBot', 'CC']

SERVER_BOT_ALLOWED = os.getenv('SERVER_BOT_ALLOWED', '')

SERVER_POSIONED_PATHS = [
    '/.aws/credentials',
    '/.dockerignore',
    '/.env',
    '/.env.backup',
    '/.env.dev',
    '/.env.example',
    '/.env.local',
    '/.env.production',
    '/.env.test',
    '/.gitignore',
    '/.htaccess',
    '/.info',
    '/.npmrc',
    '/.phpinfo',
    '/admin.php',
    '/admin.php?dispatch=auth.login_form&return_url=admin.php',
    '/admin/.env',
    '/api/.env',
    '/api-docs',
    '/app.js',
    '/app/.env',
    '/application.yml',
    '/auth.json',
    '/aws.yml',
    '/aws.yaml',
    '/aws_credentials.js',
    '/aws_credentials.json',
    '/backend/.env',
    '/backup.env',
    '/backup.sql',
    '/backup.tar.gz',
    '/backup.zip',
    '/blog/wp-includes/wlwmanifest.xml',
    '/bundle.js',
    '/CHANGELOG.txt',
    '/cloud-config.yml',
    '/cms/wp-includes/wlwmanifest.xml',
    '/composer.json',
    '/config.inc.php',
    '/config.js',
    '/config.json',
    '/config.old.php',
    '/config.php',
    '/config.xml',
    '/config.yaml',
    '/config.yml',
    '/config/.env',
    '/configuration.php~',
    '/console-config.js',
    '/credentials.env',
    '/crm/.env',
    '/crossdomain.xml',
    '/css.php?css=xenforo,form,public',
    '/database.json',
    '/database.sql',
    '/database_backup.sql',
    '/db.ini',
    '/db_backup.sql',
    '/debug.php',
    '/development.env',
    '/docker-compose.yml',
    '/Dockerfile',
    '/dump.sql',
    '/elfinder/php/connector.minimal.php',
    '/env.backup',
    '/env.txt',
    '/info.php',
    '/kjasdhaskdjhasfkjgafhjsfkjashfasf.png',
    '/local_settings.py',
    '/login',
    '/manifest.json',
    '/media/.env',
    '/npmrc',
    '/openapi.json',
    '/package.json',
    '/php.ini',
    '/phpcs.xml.dist',
    '/phpinfo',
    '/phpinfo.php',
    '/phpinfo1.php',
    '/phpinfo2.php',
    '/prod.env',
    '/secrets.json',
    '/secure-config.json',
    '/server.js',
    '/server.key',
    '/server-status',
    '/server/.env',
    '/settings.bak',
    '/settings.py',
    '/settings.yaml',
    '/settings.yml',
    '/shop/wp-includes/wlwmanifest.xml',
    '/sjakdhaskjdhakjsdhkjasd.png',
    '/sjdhaskjdhasdasdas.png',
    '/site/wp-includes/wlwmanifest.xml',
    '/stage.env',
    '/stage/.env',
    '/staging.env',
    '/stylesheet.css',
    '/stylesheet.php?cssid=123',
    '/swagger-ui.html',
    '/swagger.json',
    '/test.php',
    '/test/wp-includes/wlwmanifest.xml',
    '/twilio/.env',
    '/vendor/.env',
    '/web.config',
    '/web/wp-includes/wlwmanifest.xml',
    '/wordpress/wp-includes/wlwmanifest.xml',
    '/wp-config-sample.php',
    '/wp-config.php',
    '/wp-config.php.swp',
    '/wp-includes/ID3/license.txt',
    '/wp-login.php',
    '/wp/wp-includes/wlwmanifest.xml',
    '/wp1/wp-includes/wlwmanifest.xml',
    '/xoops.css',
    '/xmlrpc.php',
    '/xmlrpc.php?rsd',
    '/2019/wp-includes/wlwmanifest.xml',
    '/2020/wp-includes/wlwmanifest.xml',
    '/2021/wp-includes/wlwmanifest.xml'
]



BOT_BOMB = 'static/server.map.xz'

def serving_bots():


    bot_user_agent = request.headers.get('User-Agent').lower()
    bot_ip = request.remote_addr

    allowed_bots = [ allowed.strip() for allowed in SERVER_BOT_ALLOWED.split(',') if allowed.strip() ]

    if any( allowed.lower() in bot_user_agent for allowed in allowed_bots):

        return None
    
    if any( keyword.lower() in bot_user_agent for keyword in SERVER_BOT_KEYS) or SERVER_POSIONED_PATHS:

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

