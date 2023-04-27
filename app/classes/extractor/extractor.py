import datetime
import inspect

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
        file = str(inspect.stack()[1].filename.split("/")[-1]).replace(".py", "")
        filename = f'{self.TEMP_DATA_PATH}/{file}'
        file_from_url(url, filename)