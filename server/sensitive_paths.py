import re

"""
These are routes that have been under attack by bots / pentesters / lammers,
for several weeks (2025May).

Just like in the other stablished cases in nukebots.py, attackers will receive
a honeypot.

If everything works as intended, they shouldn't come back.

# pending:

1. Py list to JSON
2. 
"""
SERVER_POISONED_PATHS = [
    '/api-key*',
    '/api-secret*',
    '/.aws/*',
    '/.dockerignore',
    '/.env*',
    '/.gitignore',
    '/.htaccess',
    '/.info',
    '/.npmrc',
    '/.phpinfo',
    '/.vsc*/',
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
    '/azure*',
    '/backend/.env',
    '/backup*',
    '/backup*/',
    '/blog/*',
    '/bundle.js',
    '/CHANGELOG.txt',
    '/cloud-config.yml',
    '/cms/*',
    '/composer.json',
    '/config*',
    '/config/*',
    '/console-config.js',
    '/credentials.env',
    '/crm/*',
    '/crossdomain.xml',
    '/css.php?css=xenforo,form,public',
    '/database*',
    '/db*',
    '/debug.php',
    '/development.env',
    '/docker-compose.yml',
    '/Dockerfile',
    '/dump.sql',
    '/elfinder/*',
    '/env.backup',
    '/env.txt',
    'firebase*',
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
    '/php*.*'
    '/prod.env',
    '/secrets.json',
    '/secure-config.json',
    '/server.js',
    '/server.key',
    '/server-status',
    '/server/*',
    '/settings.bak',
    '/settings.py',
    '/settings.yaml',
    '/settings.yml',
    '/shop/*',
    '/sjakdhaskjdhakjsdhkjasd.png',
    '/sjdhaskjdhasdasdas.png',
    '/site/wp*/*',
    '/stage.env',
    '/stage/*',
    '/staging.env',
    '/stylesheet.css',
    '/stylesheet.php?cssid=123',
    '/swagger-ui.html',
    '/swagger.json',
    '/test.php',
    '/test/*',
    '/twilio/.env',
    '/vendor/*',
    '/web.config',
    '/web/*',
    '/wordpress*',
    '/wordpress/*',
    '/wp*',
    '/wp*/*',
    '/xoops.css',
    '/xmlrpc.php',
    '/xmlrpc.php?rsd',
    '/201*/*',
    '/202*/*'
]

def sensitive_REGEX(pattern):
    pattern = re.escape(pattern).replace(r'\*', '.*')
    return re.compile(f'^{pattern}$')

poisoned_patterns = [sensitive_REGEX(p) for p in SERVER_POISONED_PATHS]


def sensitive_match(path):
    return any(p.match(path) for p in poisoned_patterns)

