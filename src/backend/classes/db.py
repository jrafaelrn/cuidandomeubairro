import datetime
import psycopg2

class DB:

    def __init__(self):
        self.host='localhost' 
        self.port='5432' 
        self.dbname='cmb' 
        self.user='usuario' 
        self.password='senha' 
        self.connect()


    def connect(self):

        try:
            self.connect_now(self.host)
        except Exception as err:
            self.connect_now('database')
        
        #print(f"Conexão estabelecida com BD - {self.conexao}")
        self.bd_cursor = self.conexao.cursor()


    def connect_now(self, host):
        conexao_formato = f'dbname={self.dbname} user={self.user} host={host} password={self.password} port={self.port}'
        self.conexao = psycopg2.connect(conexao_formato)

    

    def insert(self, table_name: str, columns_name: list, columns_value: list, schema: str = 'cmb'): 
        
        columns_name = self.convert_list_to_string(columns_name)
        text_value = 'VALUES (' + (f'%s, ' * len(columns_value))[:-2] + ')'
           
        command = f'INSERT INTO {schema}.{table_name} ({columns_name}) {text_value} ON CONFLICT DO NOTHING'
        self.executar_comando(command, columns_value)


    def convert_list_to_string(self, list_to_convert: list) -> str:
        str_to_return = ''
        for item in list_to_convert:
            str_to_return += f'{item}, '
        return str_to_return[:-2]






    def executar_comando(self, command, values):
        
        #print(f'SQL COMANDO=|{command}|VALUES=|{values}|')

        #self.connect()
        return_bd = None
        
        self.bd_cursor.execute(f'{command}', values)
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



    def update_metadata(self, last_update_cmb, last_update_origin, origin):
    
        command = f'UPDATE metadata SET last_update_cmb = %s, last_update_origin = %s WHERE origin = %s'
        values = (last_update_cmb, last_update_origin, origin)

        self.executar_comando(command, values)
 

    def update_materialized_views(self):

        views = ['cmb.tabela_info', 'cmb.tabela_localizacoes']
        for view in views:
            command = f'REFRESH MATERIALIZED VIEW %s'
            self.executar_comando(command, (view,))

