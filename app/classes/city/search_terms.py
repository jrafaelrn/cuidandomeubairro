import os
import csv
import re
import json
import datetime
import timeit
import time
import logging

from app.classes.city.city import City
from app.classes.city.search_locations import search_local


log = logging.getLogger(__name__)
STATISTICS_PATH = 'statistics'



def search_all_terms(line: str):

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







if __name__ == '__main__':

    log.debug(f"Starting at {datetime.datetime.now().strftime('%H:%M:%S')}")

    # 1 - Load terms into memory
    load_terms(TERMS_FILE)

    # 2 - Search for terms in the files
    start_search()

    log.debug(f"Finished at {datetime.datetime.now().strftime('%H:%M:%S')}")
