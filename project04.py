############################################################################
# Project 04: Same AMSTRAD Colour converter tool as Project03,
# but using Python for the data process.
#
# Imports: 
from flask import Blueprint, jsonify, request
############################################################################
# 04 Logic
###############
# app.route to Blueprint added
project04 = Blueprint('project04', __name__)
###############
# Return data processed via POST
@project04.route('/convert', methods=['POST'])
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