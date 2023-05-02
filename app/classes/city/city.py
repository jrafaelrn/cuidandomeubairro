import pandas as pd
import logging
import datetime
import json


from lowercase import lowercase_text
from undecode import undecode_text
from classes.extractor.extractor import Extractor


log = logging.getLogger(__name__)



class City:
    
    def __init__(self, name: str, code: str, save_statistics: bool = False):
        self.name = name
        self.terms = {}
        self.total_rows = 0
        self.code = code
        self.locations_variations = {}
        self.save_statistics = save_statistics
        
    
    def transform(self, data: pd.DataFrame, config_columns):
        
        text = ''
        text = lowercase_text(text)
        text = undecode_text(text)
        
        
    
    def load(self):
        self.send_to_db()
        self.update_metadata()
    
    
    
    def send_to_db(self):
        pass
        
    
    
    def update_metadata(self):
        
        last_update = datetime.datetime.now()
        self.save_statistics()    
    
        
    '''
    ############# 3 #############
        
    Save statistics in CSV and JSON by default
    Optional: parameter 'format=json' or 'format=csv'

    Args:
        filename: The file to save the statistics to.
        format: The format to save the statistics in. 

    Raises:
        FileNotFoundError: If the output directory does not exist.

    '''
    def save_statistics(self, format: str = None):
        
        # Return if the user does not want to save the statistics
        if not self.save_statistics:
            return
        
        # Check if the format was specified        
        if format == 'json':
            self.save_statistics_json()
            return

        if format == 'csv':
            self.save_statistics_csv()
            return

        # Default behavior: save in both formats
        self.save_statistics_json()
        self.save_statistics_csv()
        
    
    

    def save_statistics_json(self):

        statistics = self.terms_statistics_to_dict()
        filename = self.get_file_name().replace('.csv', '')
        log.debug(f'Saving statistics in JSON...: {filename}')

        global STATISTICS_PATH
        filename = f'{STATISTICS_PATH}/json/{filename}.json'

        with open(filename, 'w', encoding='utf-8') as f:
            data = json.dumps(statistics, indent=4, ensure_ascii=False)
            f.write(data)



    def save_statistics_csv(self):

        global STATISTICS_PATH
        global locations_variation
        statistics = self.terms_statistics_to_dict()
        filename = f'{STATISTICS_PATH}/csv/{self.get_file_name()}.csv'
        log.debug(f'Saving statistics in CSV...: {filename}')

        with open(filename, 'w') as f:
            header = 'cod_cidade;cidade;termo;frequencia\n'
            f.write(header)
            content = []

            for term, quantity in statistics.items():
                if term == 'cod_cidade':
                    continue
                line = f'{self.code};{self.name};{term};{quantity}\n'
                content.append(line)
                
            # Loop through the locations variation
            for variation, quantity in locations_variation.items():
                line = f'{self.code};{self.name};variation_{variation};{quantity}\n'
                content.append(line)

            f.writelines(content)

                
        
        
    
    def etl(self, extractor: Extractor = None, data: pd.DataFrame = None, config_columns = None):        
    
        if extractor:
            data = extractor.download()
    
        self.transform(data, config_columns)
        self.load()

            
  
        
        
        
        
    def update_term(self, term):
        self.terms[term] = self.terms.get(term, 0) + 1
        
    def terms_statistics_to_dict(self):
        self.terms['total_rows'] = self.total_rows
        self.terms['cod_cidade'] = self.code        
        return self.terms
    
    
    def set_total_rows(self, total_rows):
        self.total_rows = total_rows
        
        
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