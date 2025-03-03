from flask import Flask, render_template, request, jsonify
import requests
import datetime
from bs4 import BeautifulSoup


app = Flask(__name__)


# Projects

projects = [
    {'id': '01', 'title': 'Simple Hello World', 'desc' : 'A simple Hello World using Python as a back-end, with no html.'},
    {'id': '02', 'title': 'A More Complex Hello World', 'desc' : 'CSS parallax floating bubbles saying Hello World'},
    {'id': '03', 'title': 'BackEnd only as server', 'desc' : 'App Test 01: AMSTRAD Color Tool converter, using JavaScript'},
    {'id': '04', 'title': 'BackEnd as LOGIC', 'desc' : 'App Test 02: AMSTRAD Color Tool converter, using Python'},
    {'id': '05', 'title': 'InspectorView Demo', 'desc' : 'Web CSS Inspector Tool idea'},
    {'id': '06', 'title': 'Naiz Headlines, Now', 'desc' : 'A news&headlines scrapping tool using \'requests\''},
    {'id': '404', 'title': 'Not every mistake is really a mistake' , 'desc' : '404'},
]



# @app.routes use Jinja when compatible, otherwhise set app.route('/XX') BEFORE the Jinja routes
@app.route('/')
def home():
    return render_template('main.html', projects=projects)

@app.route('/<project_id>/')
def render_project(project_id):
    try:
        return render_template(f'{project_id}/index_{project_id}.html')
    except:

        return render_template('404/index_404.html')

# 01 logic
@app.route('/01/')
def render_project_01():
        return hello_world_backend()

def hello_world_backend():
    return """<html>
    <body>
    <h1>Hello World testing app</h1>
    <p>This 'Hello World' screen is being loaded and served using Python<p>
    </body>
    </html>"""

# 02 Logic
#

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
    
# 06 Logic

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

        title = title_tag.get_text(strip=True) if title_tag else "Sin título"
        link = link_tag['href'] if link_tag else "#"
        author = author_tag.get_text(strip=True) if author_tag else "Desconocido"
        image = image_tag['src'] if image_tag else "https://via.placeholder.com/300"

        # Convertir URL relativa en absoluta
        if link.startswith("/"):
            link = url + link
        if image.startswith("/"):
            image = url + image

        titularrak.append({
            'title': title,
            'link': link,
            'author': author,
            'image': image,
            'date': datetime.datetime.now().strftime("%Y-%m-%d")
        })

    return titularrak



# main serve logic
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

    