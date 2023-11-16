import datetime
import pandas as pd
import logging

from unidecode import unidecode
from .statistics import Statistics
from classes.extractor.extractor import Extractor
from classes.transformer.transformer import Transformer
from classes.loader.loader import Loader


log = logging.getLogger(__name__)


class City:
    
    def __init__(self, name: str, code: str, origin: str, save_statistics: bool = False):
        self.name = name
        self.code = code
        self.despesas = []
        self.save_statistics = save_statistics
        self.statistics = Statistics()
        self.level_bar = 1
        self.default_locations = {}
        self.origin = origin
        self.last_update_origin = None
        
    

    def etl(self, extractor: Extractor = None, data: pd.DataFrame = None, config_columns = None):        
    
        if extractor:
            self.data = extractor.download()
            self.last_update_origin = extractor.last_update
        else:
            self.data = data
            self.last_update_origin = datetime.datetime.now()
    
        #Transformer().transform(self, config_columns)
        
        Loader().load(self)

        log.info('ETL -- SUCCESSFULLY FINISHED')
    
        

    ###########################################################
    ###########################################################

    # File Path
    def set_file_path(self, file_path):
        self.file_path = file_path
        
    def get_file_path(self):
        return self.file_path
    
    
    def get_file_name(self):
        # Get name from full path and remove the extension
        file_name = self.file_path.split('/')[-1]
        file_extension = file_name.split('.')[-1]
        return file_name.replace(f'.{file_extension}', '')
    
    
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    
    def __str__(self) -> str:
        return self.name