import logging
import os

log = logging.getLogger(__name__)
FILE_PATH = os.path.abspath(__file__)
FOLDER_PATH = os.path.dirname(FILE_PATH)
STATISTICS_PATH = f'{os.path.dirname(os.path.dirname(FOLDER_PATH))}/data_temp/statistics'

class Statistics:
    
    def __init__(self) -> None:
        self.total_lines = 0
        self.total_unique_descriptions = 0
        self.terms = {}
    
    
    def add_term(self, term):
        values = {}
        values['total_terms'] = 0
        values['total_locations'] = 0
        values['total_fake_locations'] = 0
        values['total_money'] = 0
        self.terms[term] = values
        #log.debug(f'Added term {term}')
        return self.terms[term]  
    
    
    def update_term(self, term: str, condition: str):
        
        term_target = self.terms.get(term, None)
        
        if term_target is None:
            term_target = self.add_term(term)
                        
        term_target[condition] = term_target.get(condition, 0) + 1
        
        
        
    '''        
    Save statistics in CSV and JSON by default
    Optional: parameter 'format=json' or 'format=csv'

    Args:
        filename: The file to save the statistics to.
        format: The format to save the statistics in. 

    Raises:
        FileNotFoundError: If the output directory does not exist.

    '''
    def save_statistics(self, file_name:str, format: str = None):
        
        # Return if the user does not want to save the statistics
        if not self.save_statistics:
            return
        
        # Check if the format was specified        
        if format == 'json':
            #self.save_statistics_json()
            return

        if format == 'csv':
            self.save_statistics_csv()
            return

        # Default behavior: save in both formats
        #self.save_statistics_json()
        self.save_statistics_csv(file_name)
        
    
    

    def save_statistics_json(self):

        statistics = self.terms_statistics_to_dict()
        filename = self.get_file_name().replace('.csv', '')
        log.debug(f'Saving statistics in JSON...: {filename}')

        filename = f'{STATISTICS_PATH}/json/{filename}.json'

        with open(filename, 'w', encoding='utf-8') as f:
            data = json.dumps(statistics, indent=4, ensure_ascii=False)
            f.write(data)



    def save_statistics_csv(self, file_name: str):
        
        FOLDER_CSV = f'{STATISTICS_PATH}/csv'
        
        # Save resume data
        FOLDER_RESUME = f'{FOLDER_CSV}/resume'
        filename = f'{FOLDER_RESUME}/{file_name}.csv'
        log.debug(f'Saving statistics in CSV...: {filename}')
        
        with open(filename, 'w') as f:
            f.write('city_code;total_lines;total_unique_descriptions\n')
            f.write(f'{file_name};{self.total_lines};{self.total_unique_descriptions}\n')
        
        
        # Save detailed data about terms   
        FOLDER_DETAIL = f'{FOLDER_CSV}/detail'
        filename = f'{FOLDER_DETAIL}/{file_name}.csv'
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

    
    