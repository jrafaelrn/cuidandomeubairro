import pandas as pd
import csv
import logging
import datetime
import os



log = logging.getLogger(__name__)

# Set pandas options para considerar '' como null
pd.options.mode.use_inf_as_na = True


statistics = []
total_rows = 0
empty_rows = 0
total_cities = 0
total_lines = 0
CODE_CITY_COLUMN = 3
NAME_CITY_COLUMN = 2



def slice_tce_dataset(file_path: str, folder_path):
    
    log.debug(f'=> Starting slice file {file_path}')
    
    enc = 'ISO-8859-1'
    
    with open(file_path, newline='', encoding=enc) as csvfile:
        
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        
        # Add the header to the statistics
        header = next(reader)
        statistics_struture(header)                            
        
        # Init the variables
        chunk_size = 100000
        chunk = []
        city_code = ''
        city_name = ''
        
        for i, row in enumerate(reader):
            
            if city_code == '':
                city_code = row[CODE_CITY_COLUMN]                
            
            # Check if city is the same
            # If not, save the current chunk
            if city_code != row[CODE_CITY_COLUMN]:                
                save_city(header, chunk, city_name, folder_path)
                
                # Reset the variables
                city_code = row[CODE_CITY_COLUMN]
                chunk = []
            
            chunk.append(row)
            city_name = f'{city_code}-{row[NAME_CITY_COLUMN]}'
        
        save_city(header, chunk, city_name)
        
        

def save_city(header, data, cidade_name, folder_path):
    
    global total_lines
    global total_cities
    total_lines += len(data)
    total_cities += 1
    log.debug(f'=> => Salvando arquivo da cidade {total_cities}: {cidade_name} => Total linhas acumuladas: {total_lines}')
    
    cidade_name = f"{cidade_name}-{datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}"
    file_path = f'{folder_path}/{cidade_name}.csv'
    
    pandas_dataset = pd.DataFrame(data, columns=header)    
    pandas_dataset.to_csv(file_path, sep=';', encoding='ISO-8859-1', index=False)





# Usado para criar a estrutura do JSON que irá salvar as estatísticas

def statistics_struture(header):
    
    for column_name in header:
        columns_statistics = {}
        columns_statistics['column_name'] = column_name
        columns_statistics['total_rows'] = 0
        columns_statistics['empty_rows'] = 0
        statistics.append(columns_statistics)      
    
    

def statistics_dataset(dataset):
    
    pandas_dataset = pd.DataFrame(dataset)
    
    for column_index in enumerate(pandas_dataset.columns):
        
        total_rows_dataset = pandas_dataset[column_index[0]].count()
        total_empty_rows_dataset = pandas_dataset[column_index[0]].isnull().sum()
        
        update_statistics(column_index[0], total_rows_dataset, total_empty_rows_dataset)
    
        
        
        
    

def update_statistics(column_index, total_rows, empty_rows):
    
    # Get the actual statistics based on the index column
    actual_statistics = statistics[column_index]

    actual_statistics['total_rows'] += total_rows
    actual_statistics['empty_rows'] += empty_rows   
    
    #log.debug(f"=> => Estatistica da coluna [{actual_statistics['column_name']}] atualizada com sucesso - Adicionado {total_rows} linhas e {empty_rows} linhas vazias")
        

def run():
    log.debug('Lendo o dataset...')
    
    
    log.debug(f'Estatística final = {statistics}')
    
    # Salva o resultado em um arquivo JSON
    with open('result.json', 'w') as f:
        f.write(f'{statistics}')

    

if __name__ == '__main__':
    run()    
