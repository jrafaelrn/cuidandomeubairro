import sys
import os

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_PATH)

from models import Despesa, Ibge
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine, func, select, MetaData


class ORM():

    def __init__(self):
        self.Base = DeclarativeBase()
        

    #########################################
    # Create a session to connect to the DB #
    #########################################

    def createConnection(self, prefered_host=None):

        try:
            if prefered_host:
                return self.createSessionHost(prefered_host)
        except:
            pass

        try:
            return self.createSessionHost(os.environ.get('POSTGRES_HOST'))
        except:
            return self.createSessionHost('localhost')



    def createSessionHost(self, host):

        url = URL.create(
            drivername='postgresql',
            username=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host=host,
            port=os.environ.get('POSTGRES_PORT'),
            database=os.environ.get('POSTGRES_DB')
        )

        engine = create_engine(url, echo=True)
        session = Session(engine)
        
        return session



    #################################################
    #        Insert data into the database          #
    #################################################

    # Need to be fixed

    def insert_ibge(self, cd_municipio, nome_municipio, populacao):
        
            session = self.createConnection("localhost")            
        
            try:
                ibge = Ibge(cd_municipio=cd_municipio, nome_municipio=nome_municipio, populacao=populacao)
                session.add(ibge)
                session.commit()
            except Exception as e:
                print(f'Error inserting ibge: {e}')
                session.rollback()
            finally:
                session.close()    



    #################################################
    #          Get data from the database           #
    #################################################

    def getDespesas_ano(self, ano):

        session = self.createConnection("localhost")
        despesas = []

        try:

            stmt = (
                select(
                    Despesa.latitude,
                    Despesa.longitude,
                    Despesa.valor_despesa,
                    Despesa.historico_despesa,
                    Despesa.id_despesa_detalhe
                ).filter(
                    Despesa.ano == ano,
                    Despesa.latitude != '',
                )
            )

            for row in session.execute(stmt):
                despesas.append(row)

        except Exception as e:
            print(f'Error getting despesas: {e}')
            despesas = []

        return despesas
    

    
    # Return like this
    #
    #    {
    #    "data": [
    #        {
    #            "code": "2022.70.10.15.451.3022.44903900.90.39.0.1020.9426",
    #            "notification_id": "cuidandodomeubairro/despesa/2022.70.10.15.451.3022.44903900.90.39.0.1020.9426",
    #            "notification_author": "cuidando-gastosabertos",
    #            "geometry": {
    #                "type": "Point",
    #                "coordinates": [
    #                    -46.458,
    #                    -23.633
    #                ]
    #            },
    #            "pa": "Projetos",
    #            "papa": "Projetos",
    #            "vl_pago": 0.0,
    #            "cd_fonte": 0,
    #            "cd_orgao": 70,
    #            "ds_fonte": "Tesouro Municipal",
    #            "ds_grupo": "INVESTIMENTOS",
    #            "ds_orgao": "Subprefeitura S\u00e3o Mateus",
    #            "cd_funcao": 15,
    #            "datafinal": "2022-06-30",
    #            "ds_funcao": "Urbanismo",
    #            "cd_despesa": 44903900,
    #            "cd_unidade": 10,
    #            "disponivel": 0,
    #            "ds_despesa": "Outros Servi\u00e7os de Terceiros - Pessoa Jur\u00eddica",
    #            "ds_unidade": "Administra\u00e7\u00e3o da Subprefeitura",
    #            "cd_elemento": 39,
    #            "cd_programa": 3022,
    #            "datainicial": "2022-01-01",
    #            "ds_programa": "Requalifica\u00e7\u00e3o e Promo\u00e7\u00e3o da Ocupa\u00e7\u00e3o dos Espa\u00e7os P\u00fablicos",
    #            "sigla_orgao": "SUB-SM",
    #            "vl_reduzido": 0.0,
    #            "cd_exercicio": 2022,
    #            "cd_subfuncao": 451,
    #            "dataextracao": "2022-06-01 02:32:12",
    #            "ds_categoria": "Despesas de Capital",
    #            "ds_subfuncao": "Infra-Estrutura Urbana",
    #            "vl_congelado": 40000.0,
    #            "vl_liquidado": 0.0,
    #            "administracao": "Direta",
    #            "cd_modalidade": 90,
    #            "ds_modalidade": "Aplica\u00e7\u00f5es Diretas",
    #            "grupo_despesa": 4,
    #            "vl_orcado_ano": 40000.0,
    #            "cd_anoexecucao": 2022,
    #            "vl_descongelado": 0.0,
    #            "vl_suplementado": 0.0,
    #            "projetoatividade": 9426,
    #            "categoria_despesa": 4,
    #            "vl_congeladoliquido": 40000.0,
    #            "vl_empenhadoliquido": 0.0,
    #            "vl_reservadoliquido": 0.0,
    #            "ds_projeto_atividade": "Revitaliza\u00e7\u00e3o e Aquisi\u00e7\u00e3o de Equipamentos na Pra\u00e7a n\u00e3o Denominada na Altura do N\u00ba 132 da Travessa Malva Pav\u00e3o, em S\u00e3o Raphael.",
    #            "vl_orcado_atualizado": 40000.0,
    #            "cd_nro_emenda_dotacao": 1020.0,
    #            "vl_suplementadoliquido": 0.0,
    #            "vl_reduzidoemtramitacao": 0.0,
    #            "vl_suplementadoemtramitacao": 0.0
    #        }
    #    ]
    #}

    def getDetailsFromCode(self, code):

        session = self.createConnection("localhost")
        data = []

        try:
            
            stmt = (
                select(
                    Despesa.latitude,
                    Despesa.longitude,
                    Despesa.valor_despesa,
                    Despesa.historico_despesa,
                    Despesa.id_despesa_detalhe
                ).filter(
                    Despesa.ano == ano,
                    Despesa.latitude != '',
                )
            )

            for row in session.execute(stmt):
                despesas.append(row)

        except Exception as e:
            print(f'Error getting despesas: {e}')
            despesas = []

        return despesas


    def get_total_rows(self):

        session = self.createConnection("localhost")

        rows = session.query(func.count(Despesa.id_despesa_detalhe)).scalar()
        return rows
    

    def get_locations_rows(self):

        session = self.createConnection("localhost")

        rows = session.query(func.count(Despesa.id_despesa_detalhe)).filter(Despesa.latitude != '').scalar()
        return rows


if __name__ == '__main__':

    orm = ORM()
    despesas = orm.getDespesas_ano(2023)
    print(despesas)