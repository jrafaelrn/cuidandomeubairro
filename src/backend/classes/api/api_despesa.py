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
    json_return = json.dumps({
    "data": [
        {
            "code": "2022.70.10.15.451.3022.44903900.90.39.0.1020.9426",
            "notification_id": "cuidandodomeubairro/despesa/2022.70.10.15.451.3022.44903900.90.39.0.1020.9426",
            "notification_author": "cuidando-gastosabertos",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -46.458,
                    -23.633
                ]
            },
            "pa": "Projetos",
            "papa": "Projetos",
            "vl_pago": 0.0,
            "cd_fonte": 0,
            "cd_orgao": 70,
            "ds_fonte": "Tesouro Municipal",
            "ds_grupo": "INVESTIMENTOS",
            "ds_orgao": "Subprefeitura S\u00e3o Mateus",
            "cd_funcao": 15,
            "datafinal": "2022-06-30",
            "ds_funcao": "Urbanismo",
            "cd_despesa": 44903900,
            "cd_unidade": 10,
            "disponivel": 0,
            "ds_despesa": "Outros Servi\u00e7os de Terceiros - Pessoa Jur\u00eddica",
            "ds_unidade": "Administra\u00e7\u00e3o da Subprefeitura",
            "cd_elemento": 39,
            "cd_programa": 3022,
            "datainicial": "2022-01-01",
            "ds_programa": "Requalifica\u00e7\u00e3o e Promo\u00e7\u00e3o da Ocupa\u00e7\u00e3o dos Espa\u00e7os P\u00fablicos",
            "sigla_orgao": "SUB-SM",
            "vl_reduzido": 0.0,
            "cd_exercicio": 2022,
            "cd_subfuncao": 451,
            "dataextracao": "2022-06-01 02:32:12",
            "ds_categoria": "Despesas de Capital",
            "ds_subfuncao": "Infra-Estrutura Urbana",
            "vl_congelado": 40000.0,
            "vl_liquidado": 0.0,
            "administracao": "Direta",
            "cd_modalidade": 90,
            "ds_modalidade": "Aplica\u00e7\u00f5es Diretas",
            "grupo_despesa": 4,
            "vl_orcado_ano": 40000.0,
            "cd_anoexecucao": 2022,
            "vl_descongelado": 0.0,
            "vl_suplementado": 0.0,
            "projetoatividade": 9426,
            "categoria_despesa": 4,
            "vl_congeladoliquido": 40000.0,
            "vl_empenhadoliquido": 0.0,
            "vl_reservadoliquido": 0.0,
            "ds_projeto_atividade": "Revitaliza\u00e7\u00e3o e Aquisi\u00e7\u00e3o de Equipamentos na Pra\u00e7a n\u00e3o Denominada na Altura do N\u00ba 132 da Travessa Malva Pav\u00e3o, em S\u00e3o Raphael.",
            "vl_orcado_atualizado": 40000.0,
            "cd_nro_emenda_dotacao": 1020.0,
            "vl_suplementadoliquido": 0.0,
            "vl_reduzidoemtramitacao": 0.0,
            "vl_suplementadoemtramitacao": 0.0
            }
        ]
    })

    return json_return




def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response




if __name__ == '__main__':
    app.run(debug=False)
