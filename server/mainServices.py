from serverModules.mail import start_server_email
from serverModules.logs import start_server_logs
from serverModules.keep import start_server_keep
from serverModules.nukebots import start_nukebots
from serverModules.telegram import telelog
import threading
from functools import partial


def get_services(app):

    return {
                'logs': {'thread': None, 'start_func': partial(start_server_logs, app)},
                'mail': {'thread': None, 'start_func': partial(start_server_email, app)},
                'nukebots': {'thread': None, 'start_func': partial(start_nukebots, app)},
                'telegram': {'thread': None, 'start_func': telelog.start_polling},
                'keep': {'thread': None, 'start_func': partial(start_server_keep, app)}
            }

class ServiceManager:
    
    
    _instance = None
    
    
    
    def __new__(cls):
    
        if cls._instance is None:
    
            cls._instance = super().__new__(cls)
            cls._instance.services = {}
    
    
        return cls._instance





    def register_services(self, app):
        
        from .mainServices import get_services
        self.services = get_services(app)

    
    
    def start_service(self, service_name):
    
        if service_name in self.services and not self.services[service_name]['thread']:
    
    
            thread = threading.Thread(
    
                target=self.services[service_name]['start_func'],
                daemon=True
            )
    
            thread.start()
    
            self.services[service_name]['thread'] = thread
    
            return True
    
    
        return False
    
    
    
    
    def stop_service(self, service_name):
    
        if service_name in self.services and self.services[service_name]['thread']:
    
            if service_name == 'telegram':
    
                telelog.stop()
    
            self.services[service_name]['thread'] = None
    
            return True
    
        return False
    
    
    
    
    def get_status(self):
    
        return {
    
            name: {
                'running': data['thread'] is not None,
                'thread_alive': data['thread'] and data['thread'].is_alive() if data['thread'] else False
            }
            for name, data in self.services.items()
        }

service_manager = ServiceManager()
