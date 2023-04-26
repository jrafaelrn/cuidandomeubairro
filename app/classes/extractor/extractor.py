import datetime

from abc import ABC, abstractmethod
from downloader import download_file_from_url as file_from_url


class Extractor(ABC):
    
    TEMP_DATA_PATH = '../../data_temp'
    
    @abstractmethod
    def get_last_update(self) -> datetime:
        pass
    
    @abstractmethod
    def download(self):
        pass
    
    
    def download_file_from_url(self, url: str):
        filename = f'{self.TEMP_DATA_PATH}/{__name__}'
        file_from_url(url, filename)