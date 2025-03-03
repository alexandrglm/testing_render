from flask import Flask, render_template, jsonify
import requests

"""
ISS JSON schema:
{
"iss_position" : {"longitude": "-123.3600", "latitude": "40.9938"},
 "message" : "success", 
 "timestamp" : 1740988052}
"""

app = Flask(__name__)

def get_ISS_is():
    url = 'http://api.open-notify.org/iss-now.json'
    response = requests.get(url).json()

    longitude = response['iss-position']['longitude']
    latitude = response['iss-position']['latitude']


    return longitude, latitude


def set_ISS_is():
    
    longitude, latitude = get_ISS_is()

    return jsonify({'longitude' : longitude, 'latitude' : latitude})



@app.route('/07/')
def index():
    return render_template('index_07.html')


if __name__ == '__main__':
    app.run(debug=True)
