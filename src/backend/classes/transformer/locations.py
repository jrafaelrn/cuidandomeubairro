import logging
import pandas as pd
import os
import re

from .terms import *
from geopy.geocoders import Nominatim
from unidecode import unidecode
from tqdm import tqdm

log = logging.getLogger(__name__)




class Locator:

    def __init__(self):
        self.geolocator = Nominatim(domain='localhost:8088', scheme='http')
        self.TOTAL_SEARCH_VARIATION = 3


    def search_all_locations(self, city):
        
        progress_bar = tqdm(total=len(city.despesas), desc=f'{city.name} - Searching all locations...', position=1, leave=False, mininterval=5)
        terms_content = Terms().load_terms()
        city.statistics.total_search_variations = self.TOTAL_SEARCH_VARIATION
        locations = {}
        
        for despesa in city.despesas:

            description = unidecode(despesa.historico_despesa.lower())
            id = despesa.id_despesa_detalhe

            # Primeiro verifica se existe algum termo "avenida, escola, etc" na linha
            terms_finded = self.search_all_terms(terms_content, description)
            
            # Se existir, procura pelas localizações
            if len(terms_finded) > 0:
                self.search_variations(despesa, terms_finded, city)

            progress_bar.update(1)            
        
        progress_bar.close()




    def search_all_terms(self, TERMS_CONTENT, line: str):

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
                



    def search_variations(self, despesa, terms_finded, city):       
            
        # Searching for the first 10 words
        next_word = 3
        
        for term in terms_finded:
            
            term_text = term['term']
            term_position = term['position']
            
            # Accumulates the total of each term found in the city
            city.statistics.update_total_term(term_text, 'total_term')
            
            text_to_search = despesa.historico_despesa
            next_word = 0
            text_from_position = despesa.historico_despesa[term_position:]
            words = text_from_position.split(' ')                    
            
            while next_word <= len(words) and next_word <= self.TOTAL_SEARCH_VARIATION:
                
                search = self.search_local(text_to_search)
                
                if search:
                    fake_address = self.check_fake_location(search.address, city.name)
                    if not fake_address:
                        city.statistics.update_location_term(term_text, f'variation_{next_word}')
                        despesa.latitude = search.latitude
                        despesa.longitude = search.longitude
                        return
        
                next_word = 3 if next_word == 0 else next_word + 1
                text_to_search = ' '.join(words[:next_word])



    def search_local(self, text: str):
        
        max_attempts = 10
        
        while max_attempts > 0:

            try:
                location_geo = self.geolocator.geocode(text, timeout=600)

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



    def check_fake_location(self, address: str, city_name: str):

        address = address.lower()
        address = unidecode(address)
        city_name = city_name.lower()
        city_name = unidecode(city_name)

        if 'sao paulo' in address and city_name in address:
            return False
        
        return True

