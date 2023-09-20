import datetime
import psycopg2

class DB:

    def __init__(self):
        self.host='localhost' 
        self.port='5432' 
        self.dbname='cmb' 
        self.user='usuario' 
        self.password='senha' 


    def connect(self):
        conexao_formato = f'dbname={self.dbname} user={self.user} host={self.host} password={self.password} port={self.port}'
        self.conexao = psycopg2.connect(conexao_formato)
        print(f"Conexão estabelecida com BD - {self.conexao}")

        self.bd_cursor = self.conexao.cursor()

    

    def insert(self, table_name: str, columns_name: list, columns_value: list): 
        
        columns_name = self.convert_list_to_string(columns_name)
        text_value = 'VALUES (' + (f'%s, ' * len(columns_value))[:-2] + ')'
           
        command = f'INSERT INTO {table_name} ({columns_name}) {text_value}'
        self.executar_comando(command, columns_value)


    def convert_list_to_string(self, list_to_convert: list) -> str:
        str_to_return = ''
        for item in list_to_convert:
            str_to_return += f'{item}, '
        return str_to_return[:-2]






    def executar_comando(self, command, values):
        
        print(f'SQL COMANDO=|{command}|VALUES=|{values}|')

        self.connect()
        return_bd = None
        
        self.bd_cursor.execute(f'{command}', values)

        try:
            return_bd = self.bd_cursor.fetchall()
        except Exception as err:
            print(f'Erro = {err}')
        
        print(f'Retorno Banco Dados = {return_bd}')
        self.save()

        return return_bd



    def save(self):
    
        self.conexao.commit()
        self.bd_cursor.close()
        self.conexao.close()



    def update_metadata(total_lines, total_unique_descriptions):
        
        last_update = datetime.datetime.now()
 