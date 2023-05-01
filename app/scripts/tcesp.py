import logging
import pandas as pd
import datetime
import os

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
            
            
    
    def get_data(self, file_path: str) -> pd.DataFrame:
        
        enc = 'ISO-8859-1'
        data_temp_path = super().get_data_temp_path()
        file_path = f'{data_temp_path}/{file_path}'

        # Open the file and convert to pandas dataframe
        data_frame = pd.read_csv(file_path, encoding=enc, sep=';', header=0, low_memory=False)
        city_name = str(data_frame['ds_municipio'].iloc[0])
        city_code = int(data_frame['codigo_municipio_ibge'].iloc[0])
        
        return data_frame, city_name, city_code
            
            

            

        
        
        

def run():
    
    extractor = Extractor_tce()
    #extractor.download()
    
    cities_files = []
    for file in os.listdir(extractor.get_data_temp_path(nivel=2)):
        if file.endswith('.csv'):
            cities_files.append(file)
     
    
    for file in cities_files:
        data_tce, city_name, city_code = extractor.get_data(file)
        city = City(name=city_name, code=city_code)
        city.etl(data=data_tce)