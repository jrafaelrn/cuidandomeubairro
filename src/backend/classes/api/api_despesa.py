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
                'cap_cor': '1',
                'state': 'atualizado',
                'uid': despesa[4],
            }
        })

    return jsonify({"type": "FeatureColletion", "features": json_despesas})




@app.route('/info', defaults={'year': None})
@app.route('/info/<year>')
@cross_origin()
def info(year):
    
    print(f'Response for year {year}')

    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    
    if year:
        return info_year(year)

    return jsonify({'data': {'years': [2023]}})


def info_year(year):

    orm = ORM()

    total = orm.get_total_rows()
    locations = orm.get_locations_rows()

    json_return = json.dumps({
            "data": {
                "rows": {
                    "total": total,
                    "mapped": locations,
                    "region": locations
                },
                "values": [
                    {
                        "name": "orcado",
                        "total": 82758515690.0,
                        "mapped": 881918948.0,
                        "region": 881918948.0
                    },
                    {
                        "name": "atualizado",
                        "total": "null",
                        "mapped": 0,
                        "region": 0
                    },
                    {
                        "name": "empenhado",
                        "total": 45647704515.66,
                        "mapped": 314230942.48,
                        "region": 314230942.48
                    },
                    {
                        "name": "liquidado",
                        "total": 25537700363.32,
                        "mapped": 159850578.52,
                        "region": 159850578.52
                    }
                ],
                "last_update": "2022-06-30"
            }
        })
    
    return json_return




@app.route('/list')
@cross_origin()
def list():

    code = request.args.get('code')
    return ""





def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response




if __name__ == '__main__':
    app.run(debug=False)
