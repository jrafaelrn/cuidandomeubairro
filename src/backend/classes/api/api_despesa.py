import os
import sys

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_PATH)


from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from orm import ORM

app = Flask(__name__)
CORS(app)


@app.route('/year/<ano>', methods=['GET'])
@cross_origin(origins=['http://localhost:8080'])
def despesas(ano):
    
    despesas = ORM().getDespesas_ano(ano)
    json_despesas = []

    for despesa in despesas:

        json_despesas.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [despesa[1], despesa[0]]
            },
            'properties': {
                'cap_cor': '1',
                'state': 'Liquidado',
                'uid': despesa[4],
            }
        })
    
    return jsonify({'type': 'FeatureCollection', 'features': json_despesas})




@app.route('/info', methods=['GET'])
@cross_origin(origins=['http://localhost:8080'])
def info(year):
    return jsonify({'data': {'years': [2023]}})


if __name__ == '__main__':
    app.run(debug=False)
