import logging
import pandas as pd

from geopy.geocoders import Nominatim
from undecode import undecode_text
from lowercase import lowercase_text
from search_terms import search_all_terms

geolocator = Nominatim(domain='localhost:8088', scheme='http')
#geolocator = Nominatim(user_agent="cmb3.0")

log = logging.getLogger(__name__)

TERMS_FILE = 'terms.txt'
TERMS_CONTENT = None



############# 1 #############

def load_terms(terms_file: str):

    global TERMS_CONTENT

    with open(terms_file, 'r') as f:
        TERMS_CONTENT = f.read().splitlines()
        TERMS_CONTENT = [lowercase_text(term) for term in TERMS_CONTENT]
        TERMS_CONTENT = [undecode_text(term) for term in TERMS_CONTENT]
        log.debug(f'Loaded {len(TERMS_CONTENT)} terms: \n {TERMS_CONTENT}')



def search_local(location: str):
    
    location = geolocator.geocode(location, timeout=10)
    
    if not location:
        return None
    
    return location





def search_all_locations(data: pd.DataFrame):
    
    # Loop over all rows
    for row in data.itertuples():
        
        terms_finded = search_all_terms(row.text)
        
        for term in terms_finded:
            