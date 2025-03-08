from flask import Flask, render_template, request, jsonify, send_from_directory, url_for # 04 05 06 07 08
import requests # 06 07 08
from bs4 import BeautifulSoup # 06
import datetime # 06
import json # 08
import os   # 08 img catcher
from datetime import datetime # 08, no es redundante
from PIL import Image

app = Flask(__name__)

############################################################################
# 08 Logic
#
#############
# 8.1 Route
#############
@app.route('/08/')
def render_project_08():
    with open('data/08/users.json', 'r') as file:
        users = json.load(file)
    return render_template('08/index_08.html', users=users)

#############
# 8.2 img profile things

## SERVE img route
@app.route('/data/08/<filename>')
def serve_image(filename):
    return send_from_directory('data/08', filename)

## GET NEW img
@app.route('/08/profile/new/<int:client_id>', methods=['GET'])
def new_profile(client_id):
    temp_image_path = img_profiler(client_id, is_temp=True)
    return jsonify({"img_profile": temp_image_path})

## Resizer + Quality method using pillow
def resize_image(image_path, size=(256, 256)):

    with Image.open(image_path) as img:

        img = img.resize(size, Image.LANCZOS)
        img.save(image_path, "JPEG", quality=50)

## viewer img logic
def img_profiler(client_id, is_temp=False):
    image_name = f'temp_{client_id}.jpeg' if is_temp else f'{client_id}.jpeg'
    image_path = os.path.join('data', '08', image_name)

    if not os.path.exists(image_path):
        try:
            response = requests.get('https://thispersondoesnotexist.com', timeout=5)
            response.raise_for_status()
            with open(image_path, 'wb') as file:
                file.write(response.content)

            resize_image(image_path)  

        except Exception as e:
            default_image_path = os.path.join('data', '08', 'default.jpeg')
            with open(image_path, 'wb') as file:
                with open(default_image_path, 'rb') as default_file:
                    file.write(default_file.read())

    return f'/data/08/{image_name}'








#############
# JSON things

def load_json():
    try:
        with open('data/08/users.json', 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        json_data = []

    users = []
    for user in json_data:
        img_profiler(user['client_id'])
        users.append(UserData(**user))
    return users

def save_json(users):
    with open('data/08/users.json', 'w') as file:
        json.dump(
            [
                {
                    "client_id": user._client_id,
                    "first_name": user._first_name,
                    "last_name": user._last_name,
                    "dob": user._dob,
                    "ident_id": user._ident_id,
                    "img_profile": "img_generated"
                } for user in users
            ], file, indent=4)

#############
# GETTER
@app.route('/08/profile', methods=['GET'])
def getter_users():
    users_ = load_json()
    
    response = jsonify(
        [
            {
                'client_id': user.client_id,
                'full_name': user.full_name,
                'dob': user.dob,
                'ident_id': user.ident_id,
                'img_profile': user.img_profile
            } for user in users_
        ]
    )
    
    response.headers['Content-Type'] = 'application/json'
    return response



#############
# SETTER (new)
@app.route('/08/profile', methods=['POST'])
def setter_users():
    profile_data = request.json

    users = load_json()
    new_client = max((user._client_id for user in users), default=0) + 1

    # Generar la imagen temporal
    temp_image_path = img_profiler(new_client, is_temp=True)

    new_profile = {
        'client_id': new_client,
        'first_name': profile_data['JS_FIRSTNAME'],
        'last_name': profile_data['JS_LASTNAME'],
        'dob': profile_data['JS_DOB'],
        'ident_id': profile_data['JS_ID'],
        'img_profile': temp_image_path
    }

    users.append(UserData(**new_profile))
    save_json(users)

    # temp IMG to /data/08/x.jpeg
    final_image_path = os.path.join('data', '08', f'{new_client}.jpeg')
    os.rename(os.path.join('data', '08', f'temp_{new_client}.jpeg'), final_image_path)

    return jsonify({'status': 'Data saved!'}), 201

#############
# EDITOR / CREATOR
@app.route('/08/profile/<int:client_id>', methods=['PUT'])
def editor_users(client_id):
    profile_data = request.json
    users = load_json()

    user_to_edit = next((user for user in users if user._client_id == client_id), None)

    if user_to_edit:
        user_to_edit._first_name = profile_data.get('JS_FIRSTNAME', user_to_edit._first_name)
        user_to_edit._last_name = profile_data.get('JS_LASTNAME', user_to_edit._last_name)
        user_to_edit._dob = profile_data.get('JS_DOB', user_to_edit._dob)
        user_to_edit._ident_id = profile_data.get('JS_ID', user_to_edit._ident_id)
        
        save_json(users)
        return jsonify({'status': 'Data updated!'}), 200

    new_profile = UserData(
        client_id=client_id,
        first_name=profile_data['JS_FIRSTNAME'],
        last_name=profile_data['JS_LASTNAME'],
        dob=profile_data['JS_DOB'],
        ident_id=profile_data['JS_ID'],
        img_profile=f"/data/08/{client_id}.jpeg"  
    )

    users.append(new_profile)
    save_json(users)

    temp_path = os.path.join('data', '08', f'temp_{client_id}.jpeg')
    final_path = os.path.join('data', '08', f'{client_id}.jpeg')
    
    if os.path.exists(temp_path):
        os.rename(temp_path, final_path)

    return jsonify({'status': 'New user created!'}), 201

#############
# DELETER
@app.route('/08/profile/<int:client_id>', methods=['DELETE'])
def deleter_users(client_id):
    users = load_json()
    user_to_delete = next((user for user in users if user._client_id == client_id), None)

    if user_to_delete:

        image_name = f'{client_id}.jpeg'
        image_path = os.path.join('data', '08', image_name)
        if os.path.exists(image_path):
            os.remove(image_path)

        users.remove(user_to_delete)
        save_json(users)
        return jsonify({'status': 'User deleted!'}), 200
    else:
        return jsonify({'status': 'User not found!'}), 404
    
#############
# Here starts __init__ class'es @property's
class UserData:
    def __init__(self, client_id, first_name, last_name, dob, ident_id, img_profile):
        self._client_id = client_id
        self._first_name = first_name
        self._last_name = last_name
        self._dob = dob
        self._ident_id = ident_id
        self._img_profile = img_profile

    @property
    def client_id(self):
        return self._client_id
    
    @property   # THis is the reason for the entire project
    def full_name(self):
        return f'{self._last_name},  {self._first_name}.'

    @property
    def dob(self):
        return f'Born on {self._dob}'

    @property
    def ident_id(self):
        return f'{self._ident_id}'
    
    @property
    def img_profile(self):
        if self._client_id == "default":
            return url_for('data', filename='08/default.jpeg')
        else:
            image_name = f'{self._client_id}.jpeg'
            image_path = os.path.join('data', '08', image_name)
            if os.path.exists(image_path):
                return f'/data/08/{image_name}'
            else:
                return url_for('data', filename='08/default.jpg')
############################################################################

            
# Server ops
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)