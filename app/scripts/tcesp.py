import logging
import pandas as pd
import datetime
import os
import multiprocessing as mp
import time

from classes.city.city import City
from classes.extractor.extractor import Extractor
from multiprocessing import Process
from tqdm import tqdm

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
            
            


def run_multiprocessing(files, extractor, config):
            
    # Variables for multiprocessing
    cores = mp.cpu_count()
    core_multiplier = 2
    log.debug(f'Running in {cores} cores...')
    processes = []
    running = 0
    completed = 0
    num_files = len(files)
    
    progress_bar = tqdm(total=num_files)

    while completed < num_files:
        while running <= (cores * core_multiplier) and len(files) > 0:

            file = files.pop(0)

            ### 2.2 ###
            p = Process(target=run_city, args=(file, extractor, config))
            processes.append(p)
            p.start()
            running += 1
            time.sleep(0.5)

        for process in processes:
            if process.is_alive():
                process.join()
            else:
                completed += 1
                running -= 1
                processes.remove(process)
                progress_bar.update(1)

    log.info(f'Finished all files!')
    progress_bar.close()
    
    
    
def run_city(file, extractor, config):
    
    log.debug(f'----- > Opening file {file}...')
    
    data_tce, city_name, city_code = extractor.get_data(file)
    city = City(name=city_name, code=city_code)
    city.etl(data=data_tce, config_columns=config)
    
    log.debug(f'----- > Finished file {file}...')






def run():
    
    extractor = Extractor_tce()
    #extractor.download()
    
    cities_files = []
    for file in os.listdir(extractor.get_data_temp_path(nivel=2)):
        if file.endswith('.csv'):
            cities_files.append(file)
            
    
    config = {
        "DESCRIPTION": "historico_despesa",
        "CITY_NAME": "ds_municipio",
        "CITY_CODE": "codigo_municipio_ibge",
    }
    
    # Filter cities
    cities_files = cities_files[:1]
    
    run_multiprocessing(cities_files, extractor, config)
     
    