import sys
import os

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_PATH))

from classes.db import DB


#####################################################
#       Insere os dados do IBGE no DB               
#   O arquivo CSV deve estar na pasta 'tables'      
#####################################################

def insert_ibge_csv():

    file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tables')
    file = os.path.join(file, 'IBGE-SP.csv')
    db = DB()

    with open(file, 'r', encoding='utf-8') as f:
        header = f.readline()
        for line in f.readlines():
            line = line.split(',')
            cd_municipio = int(line[0])
            nome_municipio = line[1]
            populacao = int(line[2])
            db.insert('f_ibge', ['cd_municipio', 'nome_municipio', 'populacao'], [cd_municipio, nome_municipio, populacao])

    print('Dados do IBGE inseridos com sucesso!')
    


##################################################################
#       Atualiza as VIEWS MATERIALIZADAS do banco de dados       #
##################################################################

def update_materialized_views():

    db = DB()
    db.update_materialized_views()




if __name__ == '__main__':
    insert_ibge_csv()