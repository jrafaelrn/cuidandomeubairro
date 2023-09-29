import logging
import pandas as pd
import os
import re

from geopy.geocoders import Nominatim
from unidecode import unidecode

geolocator = Nominatim(domain='localhost:8088', scheme='http')
#geolocator = Nominatim(user_agent="cmb3.0")


log = logging.getLogger(__name__)

FILE_PATH = os.path.abspath(__file__)
FOLDER_PATH = os.path.dirname(FILE_PATH)
TOTAL_SEARCH_VARIATION = 3


def load_terms():

    terms_file = os.path.join(FOLDER_PATH, "terms.txt")
    terms_content = None

    with open(terms_file, 'r', encoding="utf-8") as f:
        terms_content = f.read().splitlines()
        terms_content = [term.lower() for term in terms_content]
        terms_content = [unidecode(term) for term in terms_content]
        log.debug(f'Loaded {len(terms_content)} terms: {terms_content}')

    return terms_content




def search_all_locations(data: pd.DataFrame, column_id:str, column_description: str, statistics, city_name: str):
    
    terms_content = load_terms()
    statistics.total_search_variations = TOTAL_SEARCH_VARIATION
    locations = {}
    counter = 1
    
    for index, row in data.iterrows():

        description = row[column_description]
        id = row[column_id]

        # Primeiro verifica se existe algum termo "avenida, escola, etc" na linha
        terms_finded = search_all_terms(terms_content, description)

        # Debug
        if counter % round((len(data) / 10), 0) == 0:
            print(f'Progress: {round(counter / len(data) * 100, 0)}%')
        counter += 1   
        
        # Se existir, procura pelas localizações
        if len(terms_finded) > 0:
            search_variations(description, terms_finded, statistics, locations, id, city_name)

    return locations




def search_all_terms(TERMS_CONTENT, line: str):

    #console.debug(f'Searching line: {line}...')
    results = []

    for regex in TERMS_CONTENT:
        
        position = re.search(regex, line, re.IGNORECASE)
        
        if position:
            result = {}
            result['term'] = regex
            result['position'] = position.start()
            results.append(result)
    
    
    return results
            



def search_variations(text: str, terms_finded: list, statistics, locations: dict, column_id: str, city_name: str):       
        
    # Searching for the first 10 words
    next_word = 3
    
    for term in terms_finded:
        
        term_text = term['term']
        term_position = term['position']
        
        # Accumulates the total of each term found in the city
        statistics.update_total_term(term_text, 'total_term')
        
        text_to_search = text
        next_word = 0
        text_from_position = text[term_position:]
        words = text_from_position.split(' ')                    
        
        while next_word <= len(words) and next_word <= TOTAL_SEARCH_VARIATION:
            
            search = search_local(text_to_search)
            
            if search:
                fake_address = check_fake_location(search.address, city_name)
                if not fake_address:
                    statistics.update_location_term(term_text, f'variation_{next_word}')
                    locations[column_id] = search
                    return
    
            next_word = 3 if next_word == 0 else next_word + 1
            text_to_search = ' '.join(words[:next_word])



def search_local(text: str):
    
    max_attempts = 10
    
    while max_attempts > 0:

        try:
            location_geo = geolocator.geocode(text, timeout=600)

            if location_geo:        
                #log.debug(f'Found location at text: {text}\n\t => Address: {location_geo.address}\n\t =>=> Lat: {lat} - Lon: {lon}')
                return location_geo
            else:
                return False
            
        except Exception as e:
            log.error(f'Error searching location: {e}')
            print(f'Error searching location: {e}')
            max_attempts -= 1
            
    return False



def check_fake_location(address: str, city_name: str):

    address = address.lower()
    address = unidecode(address)
    city_name = city_name.lower()
    city_name = unidecode(city_name)

    if 'São Paulo' in address and city_name not in address:
        return False
    
    return True

