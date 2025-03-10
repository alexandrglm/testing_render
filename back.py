from flask import Flask, render_template, request, jsonify, send_from_directory, url_for, render_template_string # 04 05 06 07 08 JinjaCSS
import requests # 06 07 08
from bs4 import BeautifulSoup # 06
import json # 08
import os   # 08 img catcher, 09 game data loader
import datetime # 06
from PIL import Image #08


app = Flask(__name__)


# Projects

projects = [
    {'id': '01', 'title': 'The Most Complex "Simple Hello World" site', 'desc': 'No frills, no HTML fuss—just Python.'},
    {'id': '02', 'title': 'CSS Advanced Hello World', 'desc': 'A less simpler HelloWorld screen made by CSS with parallax effect and floating bubbles, fully over-hardcoded for no reason.'},
    {'id': '03', 'title': 'Back-End only as server', 'desc': 'App Test 01: AMSTRAD Color Tool converter using JavaScript.'},
    {'id': '04', 'title': 'Back-End as Logic', 'desc': 'App Test 02: AMSTRAD Color Tool converter using Python. Zero Front-end drama.'},
    {'id': '05', 'title': 'InspectorView Demo', 'desc': 'Why is this div not centered? Simple concept for a web CSS inspector tool.'},
    {'id': '06', 'title': 'Naiz Headlines, Now', 'desc': 'Scraping headlines like if I were a junior devel. Best news and headlines scraping tool using Py. "requests" from naiz.eus.'},
    {'id': '07', 'title': '(Where) Is-ISS?', 'desc': 'Yet another ISS live tracking tool using "requests" and JSON, but simplest.'},
    {'id': '08', 'title': 'Profile Info Getter/Setter', 'desc': 'An excuse to learn about __init_, __main__, @property decorators and so on, and so forth, by serving a fully "Profiles/Records" framework.'},
    {'id': '404', 'title': 'Not Every Mistake is Truly a Mistake', 'desc': 'Sometimes, mistakes are masterpieces, unlike this error 404 page. '}
]

############################################################################
# Flask logic
############################################################################
# main render
@app.route('/')
def home():
    return render_template('main.html', projects=projects)
#########################
# project routes render
@app.route('/<project_id>/')
def render_project(project_id):
    try:
    
        return render_template(f'{project_id}/index_{project_id}.html')
    
    except:

        return render_template('404/index_404.html')
#########################    
# css.jinja routes, when used, else, static routes
@app.route('/templates/<project_id>/<filename>.css')
def css_template(project_id, filename):

    css_path = f'{project_id}/{filename}.css.jinja'
    
    if not os.path.exists(os.path.join(app.template_folder, css_path)):
        return "Not found, use static/<project_id> route", 404
    
    return render_template(css_path), 200, {'Content-Type': 'text/css'}



############################################################################
# 01 logic
@app.route('/01/')
def render_project_01():

    # Estos nuevos objetos son los constructores finales
    
    heading = Headings('Zero Front-end drama')
    
    p1 = P('No HTML or CSS were harmed in the making of this Hello World screen.', style="font-style:italic;")
    p2 = P('Hello World, by the way.')
    
    heading_4 = Headings('This is how this hello world page is build', heading_type=4)
    
    code_content = '''

# Enjoy reading code
def render():

    heading = Headings('Zero Front-end drama')
    p1 = P('No HTML or CSS were harmed in the making of this Hello World screen.', style="font-style:italic;")
    p2 = P('Hello World, by the way.')

    code_content = Code to be shown, here
    code_style = "font-style:italic; background-color:lightgray;"

    # Web Builders
    site = Site(title='title', web_elements=[])
    site.joining_web_elements(heading)
    site.joining_web_elements(p1)
    site.joining_web_elements(p2)
    site.joining_web_elements(Code(code_content, code_style))

    # Render start
    return site.render_html()

# Now, Class'es
# The Parent Class
class HtmlRender:
    def __init__(self, content):
        self.content = content

    def render_html(self):
        raise NotImplementedError('DEBUG: No está recogiendo el contenido')


# Body COntent Classes as Child Classes

class Headings(HtmlRender):
    def __init__(self, content, heading_type=1):
        super().__init__(content)
        self.heading_type = heading_type

    def render_html(self):
        return f'< h{ self.heading_type} >{ self.content}< /h{ self.heading_type} >'

    
class P(HtmlRender):
    def __init__(self, content, style=None):
        super().__init__(content)
        self.style = style

    def render_html(self):
        if self.style:
            return f'< p style="{ self.style}">< /p>'
        return f'< p >{ self.content}< /p >'

# How this code block is being projected
class Code(HtmlRender):
    def __init__(self, content, style="font-style:italic; background-color:lightgray;"):
        super().__init__(content)
        self.style = style

    def render_html(self):
        return f'< pre >< code style="{ self.style}">{ self.content}< /code >< /pre >'


# How this site is being build
class Site(HtmlRender):
    def __init__(self, title, web_elements=None):
        super().__init__('')
        self.title = title
        self.web_elements = web_elements if web_elements is not None else []

    def joining_web_elements(self, single_element):
        self.web_elements.append(single_element)

    def render_html(self):
        body_wrapped = ''
        
        for single_element in self.web_elements:
            body_wrapped += single_element.render_html() + '\\n'

        return f' ' '
< html >
    < head >
        < title >{self.title}< /title >
    < /head >
    < body >
        {body_wrapped}
    < /body >
< /html >' ' ' '''

    code_style = "font-style:italic;"

    
    # BUilding the web
    site = HelloWorldPage(title='Project 01: The most complex "Simple Hello World" site', web_elements=[])
    site.joining_web_elements(heading)
    site.joining_web_elements(p1)
    site.joining_web_elements(heading_4)
    site.joining_web_elements(Code(code_content, code_style))
    site.joining_web_elements(p2)
    

    # Rendering 
    return site.render_html()

class HtmlRender:
    def __init__(self, content):
        self.content = content

    def render_html(self):
        raise NotImplementedError('DEBUG: No está recogiendo el contenido')

class Headings(HtmlRender):
    def __init__(self, content, heading_type=1):
        super().__init__(content)
        self.heading_type = heading_type

    def render_html(self):
        return f'<h{self.heading_type}>{self.content}</h{self.heading_type}>'

class P(HtmlRender):
    def __init__(self, content, style=None):
        super().__init__(content)
        self.style = style

    def render_html(self):
        if self.style:
            return f'<p style="{self.style}">{self.content}</p>'
        return f'<p>{self.content}</p>'

class Code(HtmlRender):
    def __init__(self, content, style="font-style:italic; background-color:lightgray;"):
        super().__init__(content)
        self.style = style

    def render_html(self):
        return f'<pre><code style="{self.style}">{self.content}</code></pre>'

class HelloWorldPage(HtmlRender):
    def __init__(self, title, web_elements=None):
        super().__init__('')
        self.title = title
        self.web_elements = web_elements if web_elements is not None else []

    def joining_web_elements(self, single_element):
        self.web_elements.append(single_element)

    def render_html(self):
        body_wrapped = ''
        
        for single_element in self.web_elements:
            body_wrapped += single_element.render_html() + '\n'

        return f'''<!DOCTYPE html>
<html>
    <head>
        <title>{self.title}</title>
    </head>
    <body>
        {body_wrapped}
    </body>
</html>'''




############################################################################

############################################################################
# 02 Logic

############################################################################
# 03 Logic
@app.route('/convert', methods=['POST'])
def convert_colors():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': "No data received"}), 400

        input0 = data.get('color1')
        input1 = data.get('color2')
        input2 = data.get('color3')
        input3 = data.get('color4')

        valid_colors = {'B', 'C', 'Y', 'R'}
        if not all(c in valid_colors for c in [input0, input1, input2, input3]):
            return jsonify({'error': "Invalid color input"}), 400

        pre_block_dict = {
            "B": ['0', '0'],
            "Y": ['0', '1'],
            "C": ['1', '0'],
            "R": ['1', '1']
        }

        input0 = ''.join(pre_block_dict[input0])
        input1 = ''.join(pre_block_dict[input1])
        input2 = ''.join(pre_block_dict[input2])
        input3 = ''.join(pre_block_dict[input3])

        pre_block0 = input0 + input1
        pre_block1 = input2 + input3

        bin_int_1 = int(pre_block1, 2)
        bin_int_0 = int(pre_block0, 2)

        hex_1 = '%1X' % bin_int_1
        hex_0 = '%1X' % bin_int_0

        final = str(hex_1 + hex_0)

        return jsonify({'final_color': final})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
############################################################################

# 05 Logic

############################################################################
# 06 Logic
#
@app.route('/06/')
def render_project_06():
    articles = naiz_titularrak_orain()
    return render_template('06/index_06.html', articles=articles)

def naiz_titularrak_orain():
    url = 'https://www.naiz.eus'
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error {response.status_code} al acceder a {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    titularrak = []

    for article in articles:
        title_tag = article.find('h3', class_='article__title')
        link_tag = title_tag.find('a') if title_tag else None
        author_tag = article.find('a', class_='article__author')
        image_tag = article.find('img')

        title = title_tag.get_text(strip=True) if title_tag else "No Title"
        link = link_tag['href'] if link_tag else "#"
        author = author_tag.get_text(strip=True) if author_tag else "Unknown"
        image = image_tag['src'] if image_tag else "https://picsum.photos/300/300"

        if link.startswith("/"):
            link = url + link
        if image.startswith("/"):
            image = url + image

        titularrak.append({
            'title': title,
            'link': link,
            'author': author,
            'image': image,
            'date': datetime.now().strftime("%Y-%m-%d")
        })

    return titularrak
############################################################################


############################################################################
# 07 Logic

@app.route('/07/')
def render_project_07():
    return render_template('07/index_07.html')

@app.route('/07/iss_position')

def iss_position():
    try:
        url = 'http://api.open-notify.org/iss-now.json'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        longitude = data['iss_position']['longitude']
        latitude = data['iss_position']['latitude']

        return jsonify({'longitude': longitude, 'latitude': latitude})
    except requests.RequestException as e:
        return jsonify({'error': f"Failed to get ISS position: {e}"}), 500
############################################################################


############################################################################
# 08 Logic
from datetime import datetime # 08, no redundante
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
# 404
#############


# Server ops
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)