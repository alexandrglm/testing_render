# BackEnd 3: Python + HTML

""""
Es lo mismo que el back 2, pero la lógica se hace en back con python.

Por un lado hay que setear la config de flask para que renderice la web.
Por otra parte, la lógica del color converter en Python.
Es la parte más sencilla.

En el front, JS debe:
1. Interpretar las acciones de inputs, output y button.
2. Formar el JSON
3. Realizar el GET-FETCH como POST.
Esta parte es menos sencilla.

"""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder="front", template_folder="front")

@app.route('/')
def home():
    return render_template('index_03.html')

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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
