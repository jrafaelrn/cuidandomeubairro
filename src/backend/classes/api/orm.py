import sys
import os

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_PATH)

from models import Despesa, Ibge
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine, func, select


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
        #metadata = db.MetaData(schema=os.environ.get('POSTGRES_SCHEMA'))
        #table_despesas = db.Table('f_despesa', metadata)
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
    



if __name__ == '__main__':

    orm = ORM()
    despesas = orm.getDespesas_ano(2023)
    print(despesas)