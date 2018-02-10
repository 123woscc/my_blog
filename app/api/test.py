from flask import jsonify

from . import api


@api.route('/hello', methods=['GET'])
def hello_api():
    return jsonify(msg='hello api!')
