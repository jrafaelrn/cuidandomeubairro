import logging
import pandas as pd
import os

from geopy.geocoders import Nominatim
from unidecode import unidecode
from undecode import undecode_text
from lowercase import lowercase_text
from search_terms import search_all_terms

geolocator = Nominatim(domain='localhost:8088', scheme='http')
#geolocator = Nominatim(user_agent="cmb3.0")


log = logging.getLogger(__name__)

FILE_PATH = os.path.abspath(__file__)
FOLDER_PATH = os.path.dirname(FILE_PATH)
TOTAL_SEARCH_VARIATION = 10


def load_terms():

    terms_file = f'{FOLDER_PATH}/terms.txt'
    terms_content = None

    with open(terms_file, 'r') as f:
        terms_content = f.read().splitlines()
        terms_content = [term.lower() for term in terms_content]
        terms_content = [unidecode(term) for term in terms_content]
        log.debug(f'Loaded {len(terms_content)} terms: {terms_content}')

    return terms_content




def search_all_locations(data: pd.DataFrame, column_name: str, statistics):    
    
    terms_content = load_terms()
    statistics.total_search_variations = TOTAL_SEARCH_VARIATION
    
    for row in data[column_name]:
        
        terms_finded = search_all_terms(terms_content, row)
        
        if len(terms_finded) > 0:
            search_variations(row, terms_finded, statistics)
            



def search_variations(text: str, terms_finded: list, statistics):       
        
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
                fake_address = check_fake_location(search)
                if not fake_address:
                    statistics.update_location_term(term_text, f'variation_{next_word}')
    
            next_word = 3 if next_word == 0 else next_word + 1
            text_to_search = ' '.join(words[:next_word])



def search_local(text: str):

    location_geo = geolocator.geocode(text, timeout=60)

    if location_geo:        
        lat, lon = location_geo.latitude, location_geo.longitude
        #log.debug(f'Found location at text: {text}\n\t => Address: {location_geo.address}\n\t =>=> Lat: {lat} - Lon: {lon}')
        return location_geo.address
    
    return False



def check_fake_location(address: str):

    if 'São Paulo' in address:
        return False
    
    return True

