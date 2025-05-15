from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route('/')
def home():

    try: 
        
        return render_template('mainteinance.html')
    
    
    except Exception as e:

        print(f'DEBUG (Server/main route) -> ERROR / not rendering!!! : {str(e)}')
        return render_template('mainteinance.html')



if __name__ == '__main__':

    Flask.run(app, host='0.0.0.0', debug=True, port=8080)
    