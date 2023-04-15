import os
import csv
import re
import json
import datetime

from unidecode import unidecode
from city import City

FOLDER_PATH = 'original_data/cidades'
TERMS_FILE = 'terms.txt'
TERMS_CONTENT = None
DESCRIPTION_COLUMN = 24
CITY_COLUMN = 2
statistics = {}
total_files = 1


############# 1 #############

def load_terms(terms_file: str):

    global TERMS_CONTENT

    with open(terms_file, 'r') as f:
        TERMS_CONTENT = f.read().splitlines()
        TERMS_CONTENT = [term.lower() for term in TERMS_CONTENT]
        print(f'Loaded {len(TERMS_CONTENT)} terms: \n {TERMS_CONTENT}')



############# 2 #############

def search_from_path(folder_path: str, layout: str):

    # Loop through the files in the folder
    for file in os.listdir(folder_path):

        full_path = os.path.join(folder_path, file)

        if os.path.isfile(full_path):
            if layout == 'tcesp':
                layout_tcesp(full_path)
                #save_statistics('csv')
        



def layout_tcesp(full_path: str):

    enc = 'ISO-8859-1'
    global DESCRIPTION_COLUMN
    global total_files
    global statistics

    with open(full_path, newline='', encoding=enc) as f:

        print(f'Opening file {total_files}: {full_path}...')
        total_files += 1
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
            #print(f'Found: {regex_find}\t\t=> {row[DESCRIPTION_COLUMN]}')

            if regex_find:
                update_statistics(city, regex_find)
            
            total_lines += 1
                
        # Update the global statistics
        city.set_total_rows(total_lines)
        total_lines = 0


def create_city(city_name: str):
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
    search_from_path(FOLDER_PATH, layout='tcesp')
    
    # 3 - Save statistics in CSV and JSON by default
    # Optional: parameter 'format=json' or 'format=csv'
    save_statistics()
    
    print(f"Finished at {datetime.datetime.now().strftime('%H:%M:%S')}")
