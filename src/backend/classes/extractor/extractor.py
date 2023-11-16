import datetime
import inspect
import os
import logging
import sys
import pandas as pd

from abc import ABC, abstractmethod
from downloader import download_file_from_url as file_from_url
from unzip import unzip_data as unzip_data
from slice_tce_dateset import slice_tce_dataset as slice_dataset
from classes.db import DB

log = logging.getLogger(__name__)

class Extractor(ABC):
    
    __DATA_TEMP_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __DATA_TEMP_BASE = os.path.join(__DATA_TEMP_BASE, "data_temp")
    
    def __init__(self, unzip: bool = False, split_format:str = None, clear_data_temp: bool = True):
        self.unzip = unzip
        self.split_format = split_format
        self.clear_data_temp = clear_data_temp
        self.last_update = None
        
    
    @abstractmethod
    def get_last_update(self) -> datetime:
        pass
    
    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def get_data(self, file_path: str) -> pd.DataFrame:
        pass
    
    
    # Get the name of the file that called this method
    # This is used to create a folder with the same name in the 'data_temp' folder
    def get_file_name(self, nivel) -> str:
        
        stack = inspect.stack()
        full_stack_names = [s.filename for s in stack]  #Just for debugging
        
        stack_filename = stack[nivel].filename
        filename = stack_filename.split(os.sep)[-1].replace(".py", "")
        return filename
    
    
    
    # Full path to the temporary file    
    def get_data_temp_path(self, nivel=3) -> str:
        data_temp_path = os.path.join(self.__DATA_TEMP_BASE, self.get_file_name(nivel))
        return data_temp_path
        
    
    def download_file_from_url(self, url: str):        
        self.download_file_path = os.path.join(self.get_data_temp_path(), "original.zip")
        
        try:
            os.makedirs(self.get_data_temp_path(), exist_ok=True)
        except Exception as e:
            log.error(f'Error creating folder: {e}')
            sys.exit(1)
        
        file_from_url(url, self.download_file_path)
        
    
    def unzip_download(self):
        log.debug(f'Starting to unzip file: {self.download_file_path}')
        unzip_data(self.download_file_path, self.get_data_temp_path())
        log.debug(f'Unzipped file: {self.download_file_path} sucessfully and removed it.')
        os.remove(self.download_file_path)
        
        
    
    def slice_data(self):
        
        if self.split_format == 'csv':
            files = [file for file in os.listdir(self.get_data_temp_path()) if file.endswith('.csv')]
            log.debug(f'Files to slice: {files}')
            
            for file in files:
                file_path = os.path.join(self.get_data_temp_path(), file)
                slice_dataset(file_path, self.get_data_temp_path())
                os.remove(file_path)


    # Método para filtrar as cidades com base em parametros.
    # Caso o parametro seja 'pop', referente à populaçoa,
    # deve ser feita uma consulta no Banco de Dados para obter as cidades
    # O segundo parametro deve ser um número inteiro, que representa, por exemplo:
    # 0 => todas as cidades (sem filtro)
    # 10 => as 10 maiores cidades
    # -10 => as 10 menores cidades

    def filter_cities(self, **kwargs):
        
        if 'pop' in kwargs:
            pop = kwargs['pop']
            self.filter_city_by_pop(pop)


    def filter_city_by_pop(self, pop):
        
        db = DB()

        # Get the cities from the database
        cities = db.get_cities_by_population(pop)
        cities = [item for sublist in cities for item in sublist]
        
        # Filter the cities and delete the file
        for file in os.listdir(self.get_data_temp_path(nivel=4)):

            city_code = str(file.split('-')[0])

            if file.endswith('.csv') and city_code not in cities:
                file_path = os.path.join(self.get_data_temp_path(nivel=4), file)
                os.remove(file_path)
                
        
        