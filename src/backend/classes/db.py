import datetime
import psycopg2
import os

class DB:

    def __init__(self):
        self.host=os.environ.get('POSTGRES_HOST')
        self.port=os.environ.get('POSTGRES_PORT')
        self.dbname=os.environ.get('POSTGRES_DB') 
        self.user=os.environ.get('POSTGRES_USER') 
        self.password=os.environ.get('POSTGRES_PASSWORD')
        self.connect()


    def connect(self):

        try:
            self.connect_now(self.host)
        except Exception as err:
            self.connect_now('localhost')
        
        print(f"Conexão estabelecida com BD - {self.host}:{self.port}/{self.dbname}")
        self.bd_cursor = self.conexao.cursor()


    def connect_now(self, host):
        conexao_formato = f'dbname={self.dbname} user={self.user} host={host} password={self.password} port={self.port}'
        self.conexao = psycopg2.connect(conexao_formato)

    

    def insert(self, table_name: str, columns_name: list, columns_value: list, schema: str = 'cmb', update: bool = False, on_conflict: str = ''):
        
        columns_name = self.convert_list_to_string(columns_name)
        text_value = 'VALUES (' + (f'%s, ' * len(columns_value))[:-2] + ')'

        if update:
            command = f'INSERT INTO {schema}.{table_name} ({columns_name}) {text_value} ON CONFLICT ({on_conflict}) DO UPDATE SET {"origin"} = EXCLUDED.{"origin"}'
        else:           
            command = f'INSERT INTO {schema}.{table_name} ({columns_name}) {text_value} ON CONFLICT DO NOTHING'

        self.executar_comando(command, columns_value)


    def convert_list_to_string(self, list_to_convert: list) -> str:
        str_to_return = ''
        for item in list_to_convert:
            str_to_return += f'{item}, '
        return str_to_return[:-2]



    def executar_comando(self, command, values = None):
        
        #print(f'SQL COMANDO=|{command}|VALUES=|{values}|')

        #self.connect()
        return_bd = None
        
        if values:
            self.bd_cursor.execute(f'{command}', values)
        else:
            self.bd_cursor.execute(command)
        self.conexao.commit()

        try:
            return_bd = self.bd_cursor.fetchall()
        except Exception as err:
            #print(f'Erro = {err}')
            pass
        
        #print(f'Retorno Banco Dados = {return_bd}')
        #self.save()

        return return_bd



    def save(self):
    
        self.conexao.commit()
        self.bd_cursor.close()
        self.conexao.close()



    def update_metadata(self, last_update_cmb, last_update_origin, origin, schema: str = 'cmb'):
        self.insert(table_name='metadata',
                    columns_name=['last_update_cmb', 'last_update_origin', 'origin'],
                    columns_value=[last_update_cmb, last_update_origin, origin],
                    update=True,
                    on_conflict='origin'
                     )
 

    def update_materialized_views(self):

        views = ['cmb.tabela_info', 'cmb.tabela_localizacoes']
        for view in views:
            command = f'REFRESH MATERIALIZED VIEW {view}'
            self.executar_comando(command)


    def get_cities_by_population(self, top_filter:int):

        command = ''
        
        # select * from (select top(5) * from logins order by USERNAME ASC) a
        if top_filter > 0:
            command = f'SELECT cd_municipio FROM cmb.f_ibge ORDER BY populacao DESC LIMIT {top_filter}'
        elif top_filter < 0:
            command = f'SELECT cd_municipio FROM cmb.f_ibge ORDER BY populacao ASC LIMIT {-top_filter}'
        else:
            command = f'SELECT cd_municipio FROM cmb.f_ibge'

        return self.executar_comando(command)

