import pandas as pd
import logging
import datetime

from .locations import Locator
from unidecode import unidecode
from classes.city.despesa import Despesa

log = logging.getLogger(__name__)


class Transformer:

    def transform(self, city, config_columns):
        
        # Remove duplicates to speed up the process, lowercase and undecode and finally search for locations

        # Get just 1000 first rows (TEMP - remove before production and uncomment the next line)
        city.data_transformed = city.data[:1000]
        #city.data_transformed = city.data.drop_duplicates(subset=[config_columns[historico_despesa]])

        self.create_despesas(city, config_columns)        
        Locator().search_all_locations(city)

        log.info(f'TRANSFORM {city.name} -- SUCCESSFULLY FINISHED')

    
    
    # Cria os objetos do tipo Despesa, que serão processados e salvos no banco de dados	

    def create_despesas(self, city, config_columns):

        log.debug(f'Creating Despesas for {city.name}...')

        for index, row in city.data_transformed.iterrows():
            
            despesa = Despesa()

            # Adiciona as colunas
            for column in config_columns.keys():
                try:
                    column_dataset = config_columns[column]
                    column_type = type(despesa.__getattribute__(column))
                    value = self.convert_type(row[column_dataset], column_type)
                    despesa.__setattr__(column, value)
                except Exception as e:
                    print(f'Error on column {column} - {e}')
                    pass

            city.despesas.append(despesa)


    def convert_type(self, value, column_type):
        
        if column_type == float:
            return self.convert_to_float(value)
        
        if column_type == int:
            return self.convert_to_int(value)
        
        if column_type == datetime.datetime:
            return self.convert_to_date(value)
        
        return value


    def convert_to_date(self, date_str: str) -> datetime:
        new_value = datetime.datetime.strptime(date_str, '%d/%m/%Y')
        new_value = datetime.datetime.strftime(new_value, '%Y/%m/%d')
        return new_value
        
    def convert_to_float(self, value: str) -> float:
        new_value = value.replace(',', '.')
        new_value = float(new_value)
        return new_value
    
    def convert_to_int(self, value: str) -> int:
        new_value = int(value)
        return new_value