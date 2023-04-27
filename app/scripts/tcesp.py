import logging

from classes.city.city import City
from classes.extractor.extractor import Extractor

log = logging.getLogger(__name__)


class Extractor_tce(Extractor):
    
    
    def get_last_update(self):
        import datetime
        return datetime.datetime.now()
        

    def download(self):
        
        urls = ['https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2022.zip']
        
        for url in urls:
            continue
            #Extractor.download_file_from_url(Extractor, url)    
        
        

def run():
    
    extractor = Extractor_tce()
    data_tce = extractor.download()
    
    cities = {}
    cities['Itapira'] = 3522604
    cities['Araras'] = 3503307
    
    for city_name, city_code in cities.items():
        city = City(name=city_name, code=city_code)
        city.etl(data=data_tce)