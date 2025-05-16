from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route('/')
def home_mainteinance():

    try:

        return render_template('mainteinance.html')


    except Exception as e:

        return render_template('mainteinance.html')



if __name__ == '__main__':

    Flask.run(app, host='0.0.0.0', debug=True, port=8080)
