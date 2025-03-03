# Example 02: Front HTML-JS, Todo en JS, Back para render


from flask import Flask, render_template

app = Flask(__name__, static_folder="front", template_folder="front")

@app.route('/')

def render():
    return render_template('index_02.html')

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
