import os
import csv
import re
import json
import datetime
import multiprocessing as mp
import timeit
import time
import logging

from multiprocessing import Process, Lock, Value
from app.classes.city.city import City
from app.classes.city.search_location import search_local
from tqdm import tqdm

log = logging.getLogger(__name__)

FOLDER_PATH = 'original_data/cidades'
STATISTICS_PATH = 'statistics'

DESCRIPTION_COLUMN = 24
CITY_COLUMN = 2
CODE_CITY_COLUMN = 3

# Multiprocessing variables
total_files = Value('i', 0)
total_files.value = 1
cities = []


time_total_searchs = Value('d', 0)
time_counters_searchs = Value('i', 0)
total_success_searchs = Value('i', 0)




############# 2 #############

def start_search():

    global cities

    ### 2.1 ###
    get_cities()
    num_files = len(cities)

    # Variables for multiprocessing
    cores = mp.cpu_count()
    core_multiplier = 2
    log.debug(f'Running in {cores} cores...')
    processes = []
    running = 0
    completed = 0
    
    progress_bar = tqdm(total=num_files)

    while completed < num_files:
        while running <= (cores * core_multiplier) and len(cities) > 0:

            city = cities.pop(0)

            ### 2.2 ###
            p = Process(target=search_from_file, args=(city, 'tcesp'))
            processes.append(p)
            p.start()
            running += 1
            time.sleep(0.5)

        for process in processes:
            if process.is_alive():
                process.join()
            else:
                completed += 1
                running -= 1
                processes.remove(process)
                progress_bar.update(1)

    log.info(f'Finished all files!')
    progress_bar.close()


############# 2.1 #############

def get_cities():

    global cities
    file_paths = [os.path.join(FOLDER_PATH, file) for file in os.listdir(FOLDER_PATH)]

    # Temp filter
    file_paths = file_paths[:10]

    for file in file_paths:
        file_name = os.path.basename(file).replace('.csv', '')
        city_code = file_name.split('-')[0]
        city_name = file_name.split('-')[1]

        city = City(city_name, city_code)
        city.set_file_path(file)
        cities.append(city)


############# 2.2 #############

def search_from_file(city: City, layout: str):

    global total_files
    full_path = city.get_file_path()
    log.debug(f'Opening file {total_files.value}: {full_path}...')
    total_files.value = total_files.value + 1

    if os.path.isfile(full_path):
        if layout == 'tcesp':
            layout_tcesp(city, full_path)
            save_statistics(city)

    log.debug(f'\n----- > Finished file {full_path}...')

    global time_total_searchs
    global time_counters_searchs
    global total_success_searchs
    log.debug(f'Total time (sec): {time_total_searchs.value}')
    log.debug(f'Total searchs: {time_counters_searchs.value}')
    log.debug(f'Average time (sec): {time_total_searchs.value / time_counters_searchs.value}')
    log.debug(f'Total success searchs: {total_success_searchs.value}')
    log.debug(f'Average success searchs(%): {(total_success_searchs.value / time_counters_searchs.value) * 100}')


############# 2.3 #############

def layout_tcesp(city: City, full_path: str):

    enc = 'ISO-8859-1'
    global DESCRIPTION_COLUMN

    with open(full_path, newline='', encoding=enc) as f:

        total_lines = 0

        # Ignore the header
        reader = csv.reader(f, delimiter=';', quotechar='"')
        next(reader)

        # Loop through the file
        for i, row in enumerate(reader):

            regex_find = search_line(row[DESCRIPTION_COLUMN])

            if regex_find:
                update_statistics(city, regex_find)
            
            total_lines += 1
            

        # Update the global statistics
        city.set_total_rows(total_lines)
        total_lines = 0



def search_line(line: str):

    global TERMS_CONTENT
    #console.debug(f'Searching line: {line}...')

    for regex in TERMS_CONTENT:
        position = re.search(regex, line, re.IGNORECASE)
        if position:
            search_locations_variations(line, position)
            return regex

    return None


def update_statistics(city: City, regex_expression: str):
    city.update_term(regex_expression)


def search_locations(text: str):

    global time_total_searchs
    global time_counters_searchs
    global total_success_searchs

    start_time = time.time()
    location_geo = search_local(text)
    end_time = time.time()
    time_total_searchs.value = time_total_searchs.value + (end_time - start_time)
    time_counters_searchs.value = time_counters_searchs.value + 1

    if location_geo:
        lat, lon = location_geo.latitude, location_geo.longitude
        #log.debug(f'Found location at text: {text}\n\t => Address: {location_geo.address}\n\t =>=> Lat: {lat} - Lon: {lon}')
        total_success_searchs.value = total_success_searchs.value + 1
        return True

    return False


locations_variation = {}


def search_locations_variations(text: str, position: int):

    global locations_variation
    next_word = 3
    
    total_search = search_locations(text)
    if total_search:
        total_variation = locations_variation.get('total_variation', 0) + 1
        locations_variation['total_variation'] = total_variation
    else:
        not_found_variation = locations_variation.get('not_total_variation', 0) + 1
        locations_variation['not_total_variation'] = not_found_variation
    
    text = text[position.start():]
    words = text.split(' ')

    while next_word <= len(words) and next_word <= 10:
        text_to_search = ' '.join(words[:next_word])
        if search_locations(text_to_search):
            total_variation = locations_variation.get(next_word, 0) + 1
            locations_variation[next_word] = total_variation
        next_word += 1


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


def save_statistics(city: City, format: str = None):

    if format == 'json':
        save_statistics_json(city)
        return

    if format == 'csv':
        save_statistics_csv(city)
        return

    # Default
    save_statistics_json(city)
    save_statistics_csv(city)


def save_statistics_json(city: City):

    statistics = city.terms_statistics_to_dict()
    filename = city.get_file_name().replace('.csv', '')
    log.debug(f'Saving statistics in JSON...: {filename}')

    global STATISTICS_PATH
    filename = f'{STATISTICS_PATH}/json/{filename}.json'

    with open(filename, 'w', encoding='utf-8') as f:
        data = json.dumps(statistics, indent=4, ensure_ascii=False)
        f.write(data)


def save_statistics_csv(city: City):

    global STATISTICS_PATH
    global locations_variation
    statistics = city.terms_statistics_to_dict()
    filename = f'{STATISTICS_PATH}/csv/{city.get_file_name()}.csv'
    log.debug(f'Saving statistics in CSV...: {filename}')

    with open(filename, 'w') as f:
        header = 'cod_cidade;cidade;termo;frequencia\n'
        f.write(header)
        content = []

        for term, quantity in statistics.items():
            if term == 'cod_cidade':
                continue
            line = f'{city.code};{city.name};{term};{quantity}\n'
            content.append(line)
            
        # Loop through the locations variation
        for variation, quantity in locations_variation.items():
            line = f'{city.code};{city.name};variation_{variation};{quantity}\n'
            content.append(line)

        f.writelines(content)


if __name__ == '__main__':

    log.debug(f"Starting at {datetime.datetime.now().strftime('%H:%M:%S')}")

    # 1 - Load terms into memory
    load_terms(TERMS_FILE)

    # 2 - Search for terms in the files
    start_search()

    log.debug(f"Finished at {datetime.datetime.now().strftime('%H:%M:%S')}")
