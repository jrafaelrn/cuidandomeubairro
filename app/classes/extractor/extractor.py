import datetime
import inspect
import os
import logging

from abc import ABC, abstractmethod
from downloader import download_file_from_url as file_from_url
from unzip import unzip_data as unzip_data
from slice_tce_dateset import slice_tce_dataset as slice_dataset

log = logging.getLogger(__name__)

class Extractor(ABC):
    
    __DATA_TEMP_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/data_temp'
    
    
    def __init__(self, unzip: bool = False, split_format:str = None, clear_data_temp: bool = True):
        self.unzip = unzip
        self.split_format = split_format
        self.clear_data_temp = clear_data_temp
        
    
    @abstractmethod
    def get_last_update(self) -> datetime:
        pass
    
    @abstractmethod
    def download(self):
        pass
    
    
    # Get the name of the file that called this method
    # This is used to create a folder with the same name in the 'data_temp' folder
    def get_file_name(self, nivel) -> str:
        
        stack = inspect.stack()
        full_stack_names = [s.filename for s in stack]  #Just for debugging
        
        stack_filename = stack[nivel].filename
        filename = stack_filename.split("/")[-1].replace(".py", "")
        return filename
    
    
    
    # Full path to the temporary file    
    def get_data_temp_path(self, nivel=3) -> str:
        data_temp_path = f'{self.__DATA_TEMP_BASE}/{self.get_file_name(nivel)}'
        return data_temp_path
        
    
    def download_file_from_url(self, url: str):        
        self.download_file_path = f'{self.get_data_temp_path()}/original.zip'
        file_from_url(url, self.download_file_path)
        
    
    def unzip_download(self):
        unzip_data(self.download_file_path, self.get_data_temp_path())
        log.debug(f'Unzipped file: {self.download_file_path} and removed it')
        os.remove(self.download_file_path)
        
        
    
    def slice_data(self):
        
        if self.split_format == 'csv':
            files = [file for file in os.listdir(self.get_data_temp_path()) if file.endswith('.csv')]
            log.debug(f'Files to slice: {files}')
            
            for file in files:
                slice_dataset(f'{self.get_data_temp_path()}/{file}', self.get_data_temp_path())
                os.remove(f'{self.get_data_temp_path()}/{file}')