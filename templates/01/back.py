# Backend básico, para testear límites de render.com

from flask import Flask

app = Flask(__name__)

@app.route('/')

def hello_world_backend():
    return "<html><body><h1>Hello World testing app</h1></body></html>"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
