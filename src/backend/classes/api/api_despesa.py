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


# Endpoint 

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
                'uid': despesa[3], # coluna 'historico_despesa' conforme ordem do retorno da função
            }
        })

    return jsonify({"type": "FeatureColletion", "features": json_despesas})



# Endpoint que retorna uma lista de anos disponíveis,
# para ser usado no seletor da página principal

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


# Endpoint que retorna os totais mapeados e gastos
# para ser utilizado no gráfico de pizza na página principal

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


"""
    Retorna os dados para a tabela de informações
    que agrupa os gastos por Função Governo ou
    para a consulta de uma despesa específica quando o usuário clicar no ponto do mapa

    1) Caso seja passado o parâmetro 'year', retorna os dados da tabela
    
    2) Caso seja passado o parâmetro 'code', retorna os dados da despesa específica,
    com base na coluna 'historico_despesa'

"""

@app.route('/list')
#@app.route('/list/<year>')
#@app.route('/list/<code>')
@cross_origin()
def list():

    orm = ORM()

    year = request.args.get('year', None)

    if year is not None:
        table_info = orm.get_table_info()

        json_return = json.dumps({
                "data": table_info
            })
        
        return json_return
    
    code = request.args.get('code', None)
    
    if code is not None:        
        despesa, totais_financeiros = orm.getDetailsFromCode(code)
        despesa_return = generate_details(despesa[0], totais_financeiros)

        json_return = json.dumps({
                "data": [despesa_return]
            })  
        
        return json_return



def generate_details(despesa, totais_financeiros):

    pago = totais_financeiros.get("Valor Pago", 0.0)
    liquidado = totais_financeiros.get("Valor Liquidado", 0.0)
    empenhado = totais_financeiros.get("Empenhado", 0.0)

    return {
            "code": despesa.id_despesa_detalhe,
            "notification_id": "",
            "notification_author": "cuidando-gastosabertos",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    despesa.latitude,
                    despesa.longitude
                ]
            },
            "pa": "Projetos",
            "papa": "Projetos",
            "vl_pago": pago,
            "cd_fonte": 0,
            "cd_orgao": 0,
            "ds_fonte": despesa.ds_fonte_recurso,
            "ds_grupo": "",
            "ds_orgao": despesa.ds_orgao,
            "cd_funcao": 0,
            "datafinal": despesa.dt_emissao_despesa.strftime("%d-%m-%Y"),
            "ds_funcao": despesa.ds_funcao_governo,
            "cd_despesa": despesa.nr_empenho,
            "cd_unidade": 0,
            "disponivel": 111,
            "ds_despesa": "",
            "ds_unidade": "",
            "cd_elemento": despesa.ds_elemento.split("-")[0],
            "cd_programa": despesa.cd_programa,
            "datainicial": despesa.dt_emissao_despesa.strftime("%d-%m-%Y"),
            "ds_programa": despesa.ds_programa,
            "sigla_orgao": "",
            "vl_reduzido": 222,
            "cd_exercicio": despesa.ano,
            "cd_subfuncao": 0,
            "dataextracao": "",
            "ds_categoria": "",
            "ds_subfuncao": despesa.ds_subfuncao_governo,
            "vl_congelado": empenhado,
            "vl_liquidado": liquidado,
            "administracao": "",
            "cd_modalidade": 0,
            "ds_modalidade": "",
            "grupo_despesa": 0,
            "vl_orcado_ano": empenhado,
            "cd_anoexecucao": despesa.ano,
            "vl_descongelado": 333,
            "vl_suplementado": 444,
            "projetoatividade": 0,
            "categoria_despesa": 0,
            "vl_congeladoliquido": empenhado,
            "vl_empenhadoliquido": empenhado,
            "vl_reservadoliquido": 555,
            "ds_projeto_atividade": despesa.historico_despesa,
            "vl_orcado_atualizado": totais_financeiros.get("Empenhado", 0.0),
            "cd_nro_emenda_dotacao": 0,
            "vl_suplementadoliquido": 666,
            "vl_reduzidoemtramitacao": 777,
            "vl_suplementadoemtramitacao": 888
    }

    
# Método para liberar o CORS a cada requisição

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response




if __name__ == '__main__':
    app.run(debug=False)
