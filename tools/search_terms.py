import os
import csv
import re
import json
import datetime
import multiprocessing as mp
import time

from multiprocessing import Process, Lock, Value
from unidecode import unidecode
from city import City

FOLDER_PATH = 'original_data/cidades'
STATISTICS_PATH = 'statistics'
TERMS_FILE = 'terms.txt'
TERMS_CONTENT = None
DESCRIPTION_COLUMN = 24
CITY_COLUMN = 2
CODE_CITY_COLUMN = 3

# Multiprocessing variables
total_files = Value('i', 0)
total_files.value = 1
manager = mp.Manager()
statistics = manager.dict()
cities = {}


############# 1 #############

def load_terms(terms_file: str):

    global TERMS_CONTENT

    with open(terms_file, 'r') as f:
        TERMS_CONTENT = f.read().splitlines()
        TERMS_CONTENT = [term.lower() for term in TERMS_CONTENT]
        TERMS_CONTENT = [unidecode(term) for term in TERMS_CONTENT]
        print(f'Loaded {len(TERMS_CONTENT)} terms: \n {TERMS_CONTENT}')



############# 2 #############

def start_search():    
    
    ### 2.1 ###
    cities_files = get_cities_files()
    num_files = len(cities_files)
    
    # Variables for multiprocessing
    cores = mp.cpu_count()
    core_multiplier = 10
    print(f'Running in {cores} cores...')
    processes = []
    running = 0
    completed = 0
    
    
    while completed < num_files:        
        while running < (cores * core_multiplier) and len(cities_files) > 0:
            
            global cities
            file = cities_files.pop(0)
            city = cities[os.path.basename(file).replace('.csv', '')]
            
            ### 2.2 ###
            p = Process(target=search_from_file, args=(city, file, 'tcesp'))
            processes.append(p)            
            p.start()
            running += 1
            
        for process in processes:
            if process.is_alive():
                process.join()
            else:
                completed += 1
                running -= 1
                processes.remove(process)
        
    
    global statistics
    print(f'Finished all files. Statistics: {len(statistics)} - \n\t Content: {[stt.to_dict() for stt in statistics.values()]}')




############# 2.1 #############

def get_cities_files():
    
    global cities
    
    file_paths = [os.path.join(FOLDER_PATH, file) for file in os.listdir(FOLDER_PATH)]
    # Filter temporary files
    file_paths = file_paths[7:10]
    
    for file in file_paths:
        file_name = os.path.basename(file).replace('.csv', '')
        cities[file_name] = City(file_name)
        
    return file_paths
    
            


############# 2.1 #############

def search_from_file(city: City, full_path: str, layout: str):

    global total_files
    print(f'Opening file {total_files.value}: {full_path}...')
    total_files.value = total_files.value + 1
    
    if os.path.isfile(full_path):
        if layout == 'tcesp':
            layout_tcesp(city, full_path)
            save_statistics()
        
    print(f'-- > Finished file {full_path}...')



############# 2.2 #############

def layout_tcesp(city: City, full_path: str):

    enc = 'ISO-8859-1'
    global DESCRIPTION_COLUMN

    with open(full_path, newline='', encoding=enc) as f:

        total_lines = 0

        # Ignore the header
        reader = csv.reader(f, delimiter=';', quotechar='"')
        next(reader)

        for i, row in enumerate(reader):
            
            regex_find = search_line(row[DESCRIPTION_COLUMN])
            #print(f'\nFound: {regex_find}\t\t=> {row[DESCRIPTION_COLUMN]}')

            if regex_find:
                update_statistics(city, regex_find)
            
            total_lines += 1
                
        # Update the global statistics
        city.set_total_rows(total_lines)
        total_lines = 0
        
    print(f'Finished file {full_path}... - Statistics: {len(statistics)} - \n\t Content: {[stt.to_dict() for stt in statistics.values()]}')




def create_city(city_name: str):
    
    global statistics
    statistics_data = statistics.values()
    print(f'Statistics Length: {len(statistics)}')
    city = City(city_name)
    statistics[city_name] = city    
    
    return city



        
def search_line(line: str):

    global TERMS_CONTENT
    line = unidecode(line).lower()
    #print(f'Searching line: {line}...')
 
    for regex in TERMS_CONTENT:
        if re.search(regex, line, re.IGNORECASE):
            return regex

    return None


def update_statistics(city: City, regex_expression: str):
    city.update_term(regex_expression)

    




'''
############# 3 #############
    
Save statistics in CSV and JSON by default
Optional: parameter 'format=json' or 'format=csv'

Args:
    filename: The file to save the statistics to.
    format: The format to save the statistics in. 

Raises:
    FileNotFoundError: If the output directory does not exist.

'''

def save_statistics(filename: str, format: str = None):

    global statistics
    statistics_data = statistics.values()
    print(f'Saving statistics - Length: {len(statistics)} - Content: {statistics}')
    
    if format == 'json':
        save_statistics_json(statistics)
        return
   
    if format == 'csv':
        save_statistics_csv(statistics)
        return
    
    # Default
    save_statistics_json(statistics)
    save_statistics_csv(statistics)
        


def save_statistics_json(statistics: dict, filename: str):
    
    print('Saving statistics in JSON...')
    global STATISTICS_PATH
    filename = f'{os.path.join(STATISTICS_PATH, filename) }.json'
    
    with open(filename, 'w', encoding='utf-8') as f:         
        
        data = ''
        for city in statistics.values():
            city_dict = city.to_dict()
            data += json.dumps(city_dict, indent=4, ensure_ascii=False)
        
        f.write(data)
  
  
        
def save_statistics_csv(statistics: dict, filename: str):
    
    print('Saving statistics in CSV...')
    global STATISTICS_PATH
    filename = f'{os.path.join(STATISTICS_PATH, filename) }.csv'
    
    with open(filename, 'w') as f:
        
        header = 'cod_cidade;cidade;termo;frequencia\n' 
        f.write(header)
        content = []
        
        for city_name, city in statistics.items():
            for term, quantity in city.terms.items():
                if term == 'cod_cidade':
                    continue
                line = f'{city.code};{city_name};{term};{quantity}\n'
                content.append(line)

        f.writelines(content)



    




if __name__ == '__main__':
    
    print(f"Starting at {datetime.datetime.now().strftime('%H:%M:%S')}")

    # 1 - Load terms into memory
    load_terms(TERMS_FILE)
    
    # 2 - Search for terms in the files
    start_search()
    
    print(f"Finished at {datetime.datetime.now().strftime('%H:%M:%S')}")
