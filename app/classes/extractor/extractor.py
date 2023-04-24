import datetime
from abc import ABC, abstractmethod


class Extractor(ABC):
    
    @abstractmethod
    def get_last_update(self) -> datetime:
        pass
    
    @abstractmethod
    def download(self):
        pass