import logging
import pandas as pd
import os
import sys
import re
import threading
import time
import geopy.geocoders
geopy.geocoders.options.default_adapter_factory = geopy.adapters.RequestsAdapter

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_PATH)

from terms import *
from geopy.geocoders import Nominatim
from geopy.adapters import RequestsAdapter
from geopy.exc import GeocoderTimedOut
from unidecode import unidecode
from tqdm import tqdm

log = logging.getLogger(__name__)




class Locator:

    def __init__(self):
        self.geolocator = Nominatim(domain='localhost:8088', scheme='http', timeout=60)
        self.TOTAL_SEARCH_VARIATION = 15 # Variável responsável por definir quantas X palavras serão buscadas para localizar o endereço


    def search_all_locations(self, city):
        
        self.city = city
        number_threads = threading.active_count()
        progress_bar = tqdm(total=len(city.despesas), desc=f'{city.name} - Searching all locations...', position=city.level_bar, leave=False, mininterval=5)
        terms_content = Terms().load_terms()
        city.statistics.total_search_variations = self.TOTAL_SEARCH_VARIATION
        
        # Remove duplicatas considerando o hash do objeto
        # baseado na coluna 'historico_despesa'
        despesas = []
        for desp in city.despesas:
            if desp not in despesas:
                despesas.append(desp)
                progress_bar.update(1)            

        progress_bar.reset(total=len(despesas))
        
        for despesa in despesas:

            description = unidecode(despesa.historico_despesa.lower())
            id = despesa.id_despesa_detalhe

            # Primeiro verifica se existe algum termo "avenida, escola, etc" na linha
            terms_finded = self.search_all_terms(terms_content, description)
            
            # Se existir, procura pelas localizações
            if len(terms_finded) > 0:
                self.search_variations(despesa, terms_finded, city)
            
            # Teste - Caso não localize pelo endereço
            #else:
            
                # será usada a coluna 'ds_orgao' para localizar
                #self.check_default_location(despesa, city)


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
        next_word = 10
        
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
                
                finded = self.search_local_from_text(text_to_search, despesa, city)
                if finded:
                    return
        
                city.statistics.update_location_term(term_text, f'variation_{next_word}')
                next_word = 3 if next_word == 0 else next_word + 1
                text_to_search = ' '.join(words[:next_word])


    
    def search_local_from_text(self, text_to_search: str, despesa, city):
        
        search = self.search_local(text_to_search)
        
        if search:
            fake_address = self.check_fake_location(search.address, city.name)
            if not fake_address:
                despesa.latitude = search.latitude
                despesa.longitude = search.longitude
                return True
            
        return False
                


    def search_local(self, text: str):
    
        try:

            location_geo = self.do_geocode(text)

            if location_geo:        
                #log.debug(f'Found location at text: {text}\n\t => Address: {location_geo.address}\n\t =>=> Lat: {lat} - Lon: {lon}')
                return location_geo
            else:
                return False
            
        except Exception as e:
            message = f'\n\n!!!!! {self.city} ----------> Error searching location: {e} !!!\n\n'
            log.error(message)
            print(message)
            raise e
    


    def do_geocode(self, address, attempt=1, max_attempts=500):
        try:
            return self.geolocator.geocode(address, timeout=60)
        except GeocoderTimedOut as e:
            if attempt <= max_attempts:
                time.sleep(1)
                return self.do_geocode(address, attempt=attempt+1)
            raise e



    def check_fake_location(self, address: str, city_name: str):

        address = address.lower()
        address = unidecode(address)
        city_name = city_name.lower()
        city_name = unidecode(city_name)

        if 'sao paulo' in address and city_name in address:
            return False
        
        return True



    # Modelo das localizacoes
    # {
    #     'PREFEITURA MUNICIPAL DE CABREUVA': {        
    #         'latitude': -23.305,
    #         'longitude': -47.136
    #     },
    #     'CAMARA MUNICIPAL DE CABREUVA': {
    #         'latitude': -23.305,
    #         'longitude': -47.136
    #     }
    # }

    def check_default_location(self, despesa, city):
        
        default_location = city.default_locations.get(despesa.ds_orgao)
        
        if default_location:
            despesa.latitude = default_location['latitude']
            despesa.longitude = default_location['longitude']
        
        else:
            # Se não encontrar o endereço, tenta buscar pelo nome do órgão
            text_to_search = despesa.ds_orgao
            finded = self.search_local_from_text(text_to_search, despesa, city)

            if finded:
                city.default_locations[despesa.ds_orgao] = {
                    'latitude': despesa.latitude,
                    'longitude': despesa.longitude
                }
