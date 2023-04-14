import os
import csv
import re
import json
import datetime

from unidecode import unidecode
from city import City

FOLDER_PATH = '/home/jrrn/gits/TCC/cidades'
TERMS_FILE = 'tools/terms.txt'
TERMS_CONTENT = None
DESCRIPTION_COLUMN = 24
CITY_COLUMN = 2
statistics = {}
total_files = 1


def find_from_path(folder_path: str, layout: str):

    # Loop through the files in the folder
    for file in os.listdir(folder_path):

        full_path = os.path.join(folder_path, file)

        if os.path.isfile(full_path):
            if layout == 'tcesp':
                layout_tcesp(full_path)
        



def layout_tcesp(full_path: str):

    enc = 'ISO-8859-1'
    global DESCRIPTION_COLUMN
    global total_files

    with open(full_path, newline='', encoding=enc) as f:

        print(f'Opening file {total_files}: {full_path}...')
        total_files += 1

        reader = csv.reader(f, delimiter=';', quotechar='"')
        next(reader)

        for i, row in enumerate(reader):
            regex_find = search_line(row[DESCRIPTION_COLUMN])
            #print(f'Found: {regex_find}\t\t=> {row[DESCRIPTION_COLUMN]}')

            if regex_find:
                update_statistics(row[CITY_COLUMN], regex_find)


        


def search_line(line: str):

    global TERMS_CONTENT
    line = unidecode(line).lower()
    #print(f'Searching line: {line}...')

    for regex in TERMS_CONTENT:
        if re.search(regex, line, re.IGNORECASE):
            return regex

    return None


'''
Statistics structure:
{
    "Adamantina": {
        "av|avenida": 1,
        "praca": 5
    },
    "Araçatuba": {
        "av|avenida": 10,
        "praca": 2
    },
    ...
}
'''

def update_statistics(city_name: str, regex_expression: str):

    global statistics

    # Check if city was in the statistics, if not, create a new one
    city = statistics.get(city_name, City(city_name))

    city.update_term(regex_expression)

    # Update the global statistics
    statistics[city_name] = city



def save_statistics(format: str):

    global statistics
    
    if format == 'json':
        with open('statistics_terms.json', 'w', encoding='utf-8') as f:         
            
            data = ''
            for city in statistics.values():
                city_dict = city.to_dict()
                data += json.dumps(city_dict, indent=4, ensure_ascii=False)
            
            f.write(data)
            return
        
   
    if format == 'csv':
        with open('statistics_terms.csv', 'w') as f:
            f.write('cidade,termo,frequencia\n')
            for city_name, city in statistics.items():
                for term, quantity in city.statistics.items():
                    f.write(f'{city_name},{term},{quantity}\n')
        
        





    


def load_terms(terms_file: str):

    global TERMS_CONTENT

    with open(terms_file, 'r') as f:
        TERMS_CONTENT = f.read().splitlines()
        TERMS_CONTENT = [term.lower() for term in TERMS_CONTENT]
        print(f'Loaded {len(TERMS_CONTENT)} terms: \n {TERMS_CONTENT}')




if __name__ == '__main__':
    
    print(f"Starting at {datetime.datetime.now().strftime('%H:%M:%S')}")

    # Load terms into memory
    load_terms(TERMS_FILE)
    find_from_path(FOLDER_PATH, 'tcesp')    
    save_statistics('json'
                    )
    print(f"Finished at {datetime.datetime.now().strftime('%H:%M:%S')}")
