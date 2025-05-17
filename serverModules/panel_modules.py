import threading
from serverModules.mail import start_server_email
from serverModules.logs import start_server_logs
from serverModules.keep import start_server_keep
from serverModules.nukebots import start_nukebots
from serverModules.telegram import telelog


ACTIVE_MODULE_THREADS = {}

def start_module(name, app=None):

    if name == 'logs' and app:
    
        ACTIVE_MODULE_THREADS[name] = threading.Thread(target=start_server_logs, args=(app,), daemon=True)
    
    
    elif name == 'mail':
    
        ACTIVE_MODULE_THREADS[name] = threading.Thread(target=start_server_email, daemon=True)
    
    
    elif name == 'keep':
    
        ACTIVE_MODULE_THREADS[name] = threading.Thread(target=start_server_keep, daemon=True)
    
    
    elif name == 'nukebots':
    
        ACTIVE_MODULE_THREADS[name] = threading.Thread(target=start_nukebots, daemon=True)
    
    
    elif name == 'telegram' and app:
    
        ACTIVE_MODULE_THREADS[name] = threading.Thread(target=telelog.start_polling, daemon=True)
    
    
    else:
        return False

    ACTIVE_MODULE_THREADS[name].start()
    
    return True
