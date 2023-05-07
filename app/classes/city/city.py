import pandas as pd
import logging
import datetime

from lowercase import lowercase_text
from undecode import undecode_text
from search_locations import search_all_locations
from .statistics import Statistics
from classes.extractor.extractor import Extractor


log = logging.getLogger(__name__)


class City:
    
    def __init__(self, name: str, code: str, save_statistics: bool = False):
        self.name = name
        self.code = code
        self.save_statistics = save_statistics
        self.statistics = Statistics()
        
    

    def etl(self, extractor: Extractor = None, data: pd.DataFrame = None, config_columns = None):        
    
        if extractor:
            data = extractor.download()
    
        self.transform(data, config_columns)
        self.load()
    


    def transform(self, data: pd.DataFrame, config_columns):
        
        self.data = data
        self.column_name = config_columns['DESCRIPTION']
        
        self.data_transformed = data.drop_duplicates(subset=[self.column_name])
        self.data_transformed = lowercase_text(self.data_transformed, self.column_name)
        self.data_transformed = undecode_text(self.data_transformed, self.column_name)
        self.data_transformed = search_all_locations(self.data_transformed, self.column_name, self.statistics)
        
    
    
    def load(self):
        self.send_to_db()
        self.update_metadata()
    
    
    
    def send_to_db(self):
        pass
        
    
    
    def update_metadata(self):
        
        last_update = datetime.datetime.now()
        self.statistics.total_lines = len(self.data)
        self.statistics.total_unique_descriptions = len(self.data[self.column_name].unique())
        self.statistics.save_statistics(self.code)    
    

        
        
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