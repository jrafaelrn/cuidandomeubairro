import pandas as pd
import csv

# Set pandas options para considerar '' como null
pd.options.mode.use_inf_as_na = True

FILE_PATH = './original_data/despesas-2022.csv'

statistics = []
total_rows = 0
empty_rows = 0
total_cities = 0
total_lines = 0



def slice_tce_dataset(file_path: str):    
    
    enc = 'ISO-8859-1'
    
    with open(file_path, newline='', encoding=enc) as csvfile:
        
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        
        # Add the header to the statistics
        header = next(reader)
        statistics_struture(header)                            
        
        # Init the variables
        chunk_size = 100000
        chunk = []
        city = ''
        
        for i, row in enumerate(reader):
            
            if city == '':
                city = row[2]
            
            if city != row[2]:
                # Salva os dados atuais
                save_city(header, chunk, city)
                
                # Reseta as variáveis
                city = row[2]
                chunk = []
            
            chunk.append(row)
        
        save_city(header, chunk, city)
        
        


def save_city(header, data, cidade_name):
    
    global total_lines
    global total_cities
    total_lines += len(data)
    total_cities += 1
    print(f'=> => Salvando arquivo da cidade {total_cities}: {cidade_name} => Total linhas acumuladas: {total_lines}')
    
    pandas_dataset = pd.DataFrame(data, columns=header)
    pandas_dataset.to_csv(f'./original_data/cidades/{cidade_name}.csv', sep=';', encoding='ISO-8859-1', index=False)





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
    
    #print(f"=> => Estatistica da coluna [{actual_statistics['column_name']}] atualizada com sucesso - Adicionado {total_rows} linhas e {empty_rows} linhas vazias")
        

def run():
    print('Lendo o dataset...')
    
    slice_tce_dataset(FILE_PATH)
    print(f'Estatística final = {statistics}')
    
    # Salva o resultado em um arquivo JSON
    with open('result.json', 'w') as f:
        f.write(f'{statistics}')

    

if __name__ == '__main__':
    run()    
