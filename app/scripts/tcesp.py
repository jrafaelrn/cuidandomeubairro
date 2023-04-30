import logging
import pandas as pd
import datetime

from classes.city.city import City
from classes.extractor.extractor import Extractor

log = logging.getLogger(__name__)


class Extractor_tce(Extractor):
    
    def __init__(self):
        super().__init__(unzip=True, split_format='csv')
    
    
    def get_last_update(self):
        return datetime.datetime.now()
        

    def download(self):
        
        urls = ['https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2022.zip']
        
        for url in urls:
            super().download_file_from_url(url)
            super().unzip_download()
            super().slice_data()
            
            
    
    def get_data(self, city_code: str) -> pd.DataFrame:
        
        enc = 'ISO-8859-1'
        data_temp_path = super().get_data_temp_path()
        file_path = f'{data_temp_path}/{city_code}.csv'

        # Open the file and convert to pandas dataframe
        data_frame = pd.read_csv(file_path, encoding=enc, sep=';', header=0, low_memory=False)
        
        return data_frame
            
            

            

        
        
        

def run():
    
    extractor = Extractor_tce()
    extractor.download()
    
    cities = {}
    cities['Itapira'] = 3522604
    cities['Araras'] = 3503307
    
    for city_name, city_code in cities.items():
        data_tce = extractor.get_data(city_code)
        city = City(name=city_name, code=city_code)
        city.etl(data=data_tce)