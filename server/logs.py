# modules/server_logger.py
import os
import socket
from datetime import datetime
from flask import request
from pymongo import MongoClient

# Exclusions
EX_EXTENSION = ['.md', '.markdown', '.png', '.jpg', '.jpeg', 
                                  '.gif', '.ico', '.svg', '.webp', '.woff', 
                                  '.woff2', '.ttf', '.eot']
EX_MIME = []

EX_PATH = []

EX_IP = os.getenv('SERVER_EX_IP', '')

EX_HOST = os.getenv('SERVER_EX_HOST', '')

EX_REASON = None

# MongoDB
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS')
MONGO_HOST_1 = os.getenv('MONGO_HOST_1')
MONGO_HOST_2 = os.getenv('MONGO_HOST_2')
MONGO_HOST_3 = os.getenv('MONGO_HOST_3')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_SETS = os.getenv('MONGO_SETS')
MONGO_URI = f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST_1}:{MONGO_PORT},{MONGO_HOST_2}:{MONGO_PORT},{MONGO_HOST_3}:{MONGO_PORT}/?replicaSet={MONGO_SETS}&authSource=admin'
MONGO_SERVER_DB = os.getenv('MONGO_SERVER_DB')
MONGO_SERVER_COLLECTION = os.getenv('MONGO_SERVER_COLLECTION')

class ServerLogger:

    def __init__(self, app=None):
    
        self.app = app
        self.EX_EXTENSION = EX_EXTENSION
        self.EX_MIME = EX_MIME
        self.EX_PATH = EX_PATH
        self.EX_IP = [ ip.strip() for ip in EX_IP.split(',') if ip.strip() ]
        self.EX_HOST = [ h.strip() for h in EX_HOST.split(',') if h.strip() ]
        
        self.mongo_client = None
        self.MONGO_SERVER_DB = None

        self.start_MONGO()

    def start_MONGO(self):
        
        try:
                
            self.mongo_client = MongoClient(MONGO_URI)
            self.MONGO_SERVER_DB = self.mongo_client[MONGO_SERVER_DB]
    
            print('DEBUG (Server/Mongo) -> MongoDB connection OK!')
        
        except Exception as e:
        
            print(f'DEBUG (Server/Mongo) -> MongoDB  error: {str(e)}')

    def init_app(self, app):
        
        self.app = app
        app.before_request(self.server_logging)



    def server_logging(self):
        
        if self.MONGO_SERVER_DB is None:
        
            print('DEBUG (logging) -> No MongoDB configured!')
            return


        path = request.path.lower()
        accept_header = (request.headers.get('Accept') or '').lower()
        content_type = (request.headers.get('Content-Type') or '').lower()
        client_ip = request.remote_addr
        forwarded_for = request.headers.get("X-Forwarded-For", "")
        real_ip = forwarded_for.split(",")[0].strip() if forwarded_for else client_ip

        try:

            client_host = socket.gethostbyaddr(real_ip)[0]
        
        except socket.herror:    
            
            client_host = 'Unknown'


        '''
        Exclusions by:
        - Path
        - MIME Type / File Header -> 
        - IP -> Extracted from .env EX_IP string (non-quoted)
        - Host -> Sanitized by _host_sanitization
        
        Logging debug process started:
        - Why reason? -> then -> explained reason
        
        '''

        ex_reasons = []

        if (path in self.EX_PATH):
             
            ex_reasons.append(f'path exclusion ({path})')
            
        elif any( path.endswith(ext) for ext in self.EX_EXTENSION):
            
            ex_reasons.append(f'extension exclusion ({path})')
            
        elif any(accept_header.startswith(prefix) for prefix in self.EX_MIME):

            ex_reasons.append(f'MIME type exclusion ({accept_header})')
            
        elif real_ip in self.EX_IP:
            
            ex_reasons.append(f'IP exclusion ({real_ip})')
            
        elif self._host_sanitization(client_host):

            ex_reasons.append(f'HOST exclusion ({client_host})')

        
        if ex_reasons: 

            print(f'\n[DEBUG VISIT] -> Excluded from logs: {real_ip}\nReasons: {', '.join(ex_reasons)}\n')
            return


        visit_data = {
            "timestamp": datetime.utcnow(),
            "ip": real_ip,
            "host": client_host,
            "user_agent": request.headers.get("User-Agent"),
            "referer": request.headers.get("Referer"),
            "method": request.method,
            "path": path,
            "full_url": request.url,
            "port": request.environ.get('REMOTE_PORT'),
            "accept": accept_header,
            "content_type": content_type,
            "query_string": request.query_string.decode('utf-8') if request.query_string else None,
            "remote_user": request.remote_user,
            "content_length": request.content_length,
        }

        try:
       
            self.MONGO_SERVER_DB[os.getenv('MONGO_SERVER_COLLECTION', 'clients')].insert_one(visit_data)
            
            print(f'[VISIT] {datetime.utcnow()} - IP: {real_ip} - Host: {client_host} - Method: {request.method} - Path: {path}')
       
        except Exception as e:

            print(f'[VISIT ERROR] {datetime.utcnow()} - Error logging visit: {str(e)}')


    def _host_sanitization(self, client_host):

        return any(ex_host in client_host for ex_host in self.EX_HOST)



def start_server_logs(app):
    
    logger = ServerLogger()
    logger.init_app(app)