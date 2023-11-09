import sys
import os

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_PATH)

from models import Despesa, Ibge, TableInfo
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine, func, select, MetaData


class ORM():

    def __init__(self):
        self.Base = DeclarativeBase()
        self.engine = None
        

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

        self.engine = create_engine(url, echo=True)
        session = Session(self.engine)
        
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
    

    # Método reponsável por retornar os dados de uma despesa
    # quando o usuário clicar no ponto do mapa
    # A pesquisa é feita com base no campo 'historico_despesa'

    def getDetailsFromCode(self, code):

        session = self.createConnection("localhost")
        despesa = []

        try:
            
            stmt = (
                select(
                    Despesa.latitude,
                    Despesa.longitude,
                    Despesa.valor_despesa,
                    Despesa.historico_despesa,
                    Despesa.id_despesa_detalhe,
                    Despesa.cd_programa,
                    Despesa.ds_programa
                ).filter(
                    Despesa.historico_despesa == code,
                    Despesa.latitude != '',
                )
            )

            for row in session.execute(stmt):
                despesa.append(row)

        except Exception as e:
            print(f'Error getting despesas: {e}')
            despesa = []

        return despesa


    def get_total_rows(self):

        session = self.createConnection("localhost")

        rows = session.query(func.count(Despesa.id_despesa_detalhe)).scalar()
        return rows
    

    def get_locations_rows(self):

        session = self.createConnection("localhost")

        rows = session.query(
            func.count(Despesa.id_despesa_detalhe)
            ).filter(Despesa.latitude != '').scalar()
        
        return rows


    
    # Seleciona a tabela de informação que agrupa
    # as despesas por função de governo

    def get_table_info(self):

        session = self.createConnection("localhost")

        data = []
        table_info = session.query(TableInfo).all()

        for row in table_info:
            data.append({
                'ds_orgao': row.ds_funcao_governo,
                'vl_orcado_ano': row.planejado,
                'vl_empenhadoliquido': row.empenhado,
                'vl_liquidado': row.liquidado
            })

        return data


if __name__ == '__main__':

    orm = ORM()
    despesas = orm.getDespesas_ano(2023)
    print(despesas)