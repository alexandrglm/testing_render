from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


projects = [
    {'id': '01', 'title': 'Simple Hello World', 'desc' : 'A simple Hello World using Python as a back-end, with no html.'},
    {'id': '02', 'title': 'A More Complex Hello World', 'desc' : 'CSS parallax floating bubbles saying Hello World'},
    {'id': '03', 'title': 'BackEnd only as server', 'desc' : 'App Test 01: AMSTRAD Color Tool converter, using JavaScript'},
    {'id': '04', 'title': 'BackEnd as LOGIC', 'desc' : 'App Test 02: AMSTRAD Color Tool converter, using Python'},
    {'id': '05', 'title': 'InspectorView Demo', 'desc' : 'Web CSS Inspector Tool idea'},
    {'id': '404', 'title': 'Not every mistake is really a mistake' , 'desc' : '404'},
]

@app.route('/')
def home():
    return render_template('main.html', projects=projects)

@app.route('/01/')
def render_project_01():
        return hello_world_backend()

@app.route('/<project_id>/')
def render_project(project_id):
    try:
        return render_template(f"{project_id}/index_{project_id}.html")
    except:
        return "Page not found", 404

# 01 logic
def hello_world_backend():
    return """<html>
    <body>
    <h1>Hello World testing app</h1>
    <p>This 'Hello World' screen is being loaded and served using Python<p>
    </body>
    </html>
    """

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
    

# main serve logic
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

    