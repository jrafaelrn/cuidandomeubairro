import requests
import logging

from tqdm import tqdm
from importlib import import_module
from ..classes.city import City
from ..classes.extractor import Extractor

log = logging.getLogger(__name__)


class Extractor_tce(Extractor):

    def download(self):
        
        urls = ['https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2022.zip']
        
        for url in urls:
            file_name = url.split('/')[-1]
            self.download_data(url, f'original_data/{file_name}')        
        
        

    def download_data(self, url: str, filename: str):
        
        log.info(f"Downloading {url}...")
        
        req = requests.get(url, stream=True)
        total_size_bytes = int(req.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_bytes, unit='iB', unit_scale=True)
        
        with open(filename, 'wb') as f:
            for chunk in req.iter_content(chunk_size=block_size):
                progress_bar.update(len(chunk))            
                f.write(chunk)
        
        progress_bar.close()
        if total_size_bytes != 0 and progress_bar.n != total_size_bytes:
            log.error("ERROR, something went wrong")
        else:
            log.info(f"Downloaded {filename} successfully")
            


def run():
    
    extractor = Extractor_tce()
    data_tce = extractor.download()
    
    cities = {}
    cities['Itapira'] = 3522604
    cities['Araras'] = 3503307
    
    for city_name, city_code in cities.items():
        city = City(name=city_name, code=city_code)
        city.etl(data=data_tce)
    
    
