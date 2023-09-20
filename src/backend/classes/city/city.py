import pandas as pd
import logging
import datetime

from unidecode import unidecode
from search_locations import search_all_locations
from .statistics import Statistics
from classes.extractor.extractor import Extractor
from classes.db import DB


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

        log.info('ETL -- SUCCESSFULLY FINISHED')
    

    #################################################
    #                   TRANSFORM                   #
    #################################################

    def transform(self, data: pd.DataFrame, config_columns):
        
        self.data = data
        self.column_name_description = config_columns['DESCRIPTION']
        self.column_name_id = config_columns['ID']
        
        # Remove duplicates to speed up the process, lowercase and undecode and finally search for locations

            # Get just 500 first rows (TEMP - remove before production and uncomment the next line)
        self.data_transformed = data = data[:500]
        #self.data_transformed = data.drop_duplicates(subset=[self.column_name])
        self.data_transformed = self.lowercase_text(self.data_transformed, self.column_name_description)
        self.data_transformed = self.undecode_text(self.data_transformed, self.column_name_description)
        
        self.ids_locations = search_all_locations(self.data_transformed, self.column_name_id, self.column_name_description, self.statistics)
        
        log.info('TRANSFORM -- SUCCESSFULLY FINISHED')
    



    def lowercase_text(self, dataFrame: pd.DataFrame, column: str):

        print("Starting lowercase text...")
    
        for index, row in dataFrame.iterrows():
            dataFrame.loc[index, column] = row[column].lower()
        
        print("...Lowercase finished successfully !!")
        return dataFrame

    

    def undecode_text(self, dataFrame: pd.DataFrame, column: str) -> pd.DataFrame:

        print("Starting undecode text...")
    
        for index, row in dataFrame.iterrows():
            dataFrame.loc[index, column] = unidecode(row[column])
        
        print("...Undecode finished successfully !!")
        return dataFrame




    #################################################
    #                     LOAD                      #
    #################################################
    
    def load(self):
        DB.send_to_db(self.data_transformed)
        DB.update_metadata()

        
        
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