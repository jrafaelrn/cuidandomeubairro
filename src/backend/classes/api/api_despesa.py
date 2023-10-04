import os
import sys
import json
import geojson

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_PATH)


from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from orm import ORM

app = Flask(__name__)
CORS(app)


@app.route('/minlist/<ano>', methods=['GET'])
@cross_origin()
def despesas(ano):

    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    
    despesas = ORM().getDespesas_ano(ano)
    json_despesas = []

    for despesa in despesas:

        json_despesas.append({
            "type": "Feature",
            'geometry': {
                'coordinates': [float(despesa[1]), float(despesa[0])],
                'type': 'Point',
            },
            'properties': {
                'cap_cor': 'capital',
                'state': 'atualizado',
                'uid': despesa[4],
            }
        })
    
    json_response = {
        "FeatureCollection": json_despesas
    }

    return jsonify(json_response)




@app.route('/info', defaults={'year': None})
@app.route('/info/<year>')
@cross_origin()
def info(year):
    
    print(f'Response for year {year}')

    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()

    return jsonify({'data': {'years': [2023]}})



def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response




if __name__ == '__main__':
    app.run(debug=False)
