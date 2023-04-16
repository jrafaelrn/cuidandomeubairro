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
TERMS_FILE = 'terms.txt'
TERMS_CONTENT = None
DESCRIPTION_COLUMN = 24
CITY_COLUMN = 2

# Multiprocessing variables
total_files = Value('i', 0)
total_files.value = 1
manager = mp.Manager()
statistics = manager.dict()


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
    
    file_paths = [os.path.join(FOLDER_PATH, file) for file in os.listdir(FOLDER_PATH)]
    file_paths = file_paths[7:10]
    num_files = len(file_paths)
    
    cores = mp.cpu_count()
    core_multiplier = 10
    print(f'Running in {cores} cores...')
    processes = []
    running = 0
    completed = 0
    
    while completed < num_files:        
        while running < (cores * core_multiplier) and len(file_paths) > 0:
            
            file = file_paths.pop(0)
            p = Process(target=search_from_file, args=(file, 'tcesp'))
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
        
            
            



def search_from_file(full_path: str, layout: str):

    global total_files
    print(f'Opening file {total_files.value}: {full_path}...')
    total_files.value = total_files.value + 1
    
    if os.path.isfile(full_path):
        if layout == 'tcesp':
            layout_tcesp(full_path)
            #save_statistics('csv')
        
    print(f'-- > Finished file {full_path}...')


def layout_tcesp(full_path: str):

    enc = 'ISO-8859-1'
    global DESCRIPTION_COLUMN

    with open(full_path, newline='', encoding=enc) as f:

        total_lines = 0
        city = None

        # Ignore the header
        reader = csv.reader(f, delimiter=';', quotechar='"')
        next(reader)

        for i, row in enumerate(reader):
            
            if i == 0:
                city_name = row[CITY_COLUMN]
                city = create_city(city_name)
            
            regex_find = search_line(row[DESCRIPTION_COLUMN])
            #print(f'\nFound: {regex_find}\t\t=> {row[DESCRIPTION_COLUMN]}')

            if regex_find:
                update_statistics(city, regex_find)
            
            total_lines += 1
                
        # Update the global statistics
        city.set_total_rows(total_lines)
        total_lines = 0




def create_city(city_name: str):
    
    global statistics
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

    




############# 3 #############

def save_statistics(format: str = None):

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
        


def save_statistics_json(statistics: dict):
    with open('statistics_terms.json', 'w', encoding='utf-8') as f:         
        
        data = ''
        for city in statistics.values():
            city_dict = city.to_dict()
            data += json.dumps(city_dict, indent=4, ensure_ascii=False)
        
        f.write(data)
  
        
def save_statistics_csv(statistics: dict):
    with open('statistics_terms.csv', 'w') as f:
        header = 'cidade;termo;frequencia\n' 
        f.write(header)
        
        for city_name, city in statistics.items():
            for term, quantity in city.terms.items():
                line = f'{city_name};{term};{quantity}\n'
                f.write(line)




    




if __name__ == '__main__':
    
    print(f"Starting at {datetime.datetime.now().strftime('%H:%M:%S')}")

    # 1 - Load terms into memory
    load_terms(TERMS_FILE)
    
    # 2 - Search for terms in the files
    start_search()
    
    # 3 - Save statistics in CSV and JSON by default
    # Optional: parameter 'format=json' or 'format=csv'
    save_statistics()
    
    print(f"Finished at {datetime.datetime.now().strftime('%H:%M:%S')}")
