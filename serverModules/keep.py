############################################################################
# Flask keep-alive
################
import requests
import time

def start_server_keep():

    while True:
        try:

            elKeep = requests.get('http://ipecho.net/plain')
            print(f'DEBUG -> Server IP is:  {elKeep.text}')

        except Exception as e:

            print(f'DEBUG -> Error getting IP : {str(e)}')
            
        time.sleep(20)