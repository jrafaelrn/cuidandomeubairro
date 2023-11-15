import logging
import os
import json

log = logging.getLogger(__name__)
FILE_PATH = os.path.abspath(__file__)
FOLDER_PATH = os.path.dirname(FILE_PATH)
STATISTICS_PATH = os.path.join(os.path.dirname(os.path.dirname(FOLDER_PATH)), "data_temp", "statistics")

class Statistics:
    
    def __init__(self) -> None:
        self.total_lines = 0
        self.total_unique_descriptions = 0
        self.terms = {}
        self.total_terms = {}
        self.total_search_variations = 0
        self.check_folder(STATISTICS_PATH)
    
    
    def add_term(self, term):
        values = {}
        self.terms[term] = values
        #log.debug(f'Added term {term}')
        return self.terms[term]  
    
    
    def add_total_term(self, term):
        values = {}
        values['total_term'] = 0
        values['total_locations'] = 0
        values['total_money'] = 0
        self.total_terms[term] = values
        return self.total_terms[term]
        
    
    
    def update_location_term(self, term: str, condition: str):        
        term_target = self.terms.get(term, None)
        
        if term_target is None:
            term_target = self.add_term(term)
                        
        term_target[condition] = term_target.get(condition, 0) + 1
        
        self.update_total_term(term, 'total_locations')
            
    
    
    def update_total_term(self, term: str, condition: str):        
        term_target = self.total_terms.get(term, None)
        
        if term_target is None:
            term_target = self.add_total_term(term)
                    
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

        filename = os.path.join(STATISTICS_PATH, "json", f"{filename}.json")

        with open(filename, 'w', encoding='utf-8') as f:
            data = json.dumps(statistics, indent=4, ensure_ascii=False)
            f.write(data)



    def save_statistics_csv(self, file_name: str):
        
        FOLDER_CSV = os.path.join(STATISTICS_PATH, "csv")
        self.check_folder(FOLDER_CSV)
        
        # Save resume data
        FOLDER_RESUME = os.path.join(FOLDER_CSV, "resume")
        self.check_folder(FOLDER_RESUME)
        filename = os.path.join(FOLDER_RESUME, f'{file_name}.csv')
        log.debug(f'Saving statistics in CSV...: {filename}')
        
        with open(filename, 'w') as f:
            f.write('city_code;total_lines;total_unique_descriptions\n')
            f.write(f'{file_name};{self.total_lines};{self.total_unique_descriptions}\n')
        
        
        # Save detailed data about terms   
        FOLDER_DETAIL = os.path.join(FOLDER_CSV, "detail")
        self.check_folder(FOLDER_DETAIL)
        filename = os.path.join(FOLDER_DETAIL, f'{file_name}.csv')
        log.debug(f'Saving statistics in CSV...: {filename}')
        
        with open(filename, 'w') as f:
            header = f'city_code;term;{";".join(f"variation_{i}" for i in range(0, self.total_search_variations + 1))};\n'
            f.write(header)
            content = []

            for term, values in self.terms.items():
                
                line = f'{file_name};{term};'
                
                for variation in range(0, self.total_search_variations + 1):
                    line += f'{values.get(f"variation_{variation}", 0)};'
                
                line += '\n'
                content.append(line)

            f.writelines(content)

    
    def check_folder(self, folder_path: str):
        try:
            os.makedirs(folder_path, exist_ok=True)
        except Exception as e:
            log.warning(f'Error creating folder: {e}')
    