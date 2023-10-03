import pandas as pd
import logging

from .locations import Locator
from unidecode import unidecode

log = logging.getLogger(__name__)


class Transformer:

    def transform(self, city, config_columns):
    
        column_name_description = config_columns['DESCRIPTION']
        column_name_id = config_columns['ID']
        
        # Remove duplicates to speed up the process, lowercase and undecode and finally search for locations

        # Get just 500 first rows (TEMP - remove before production and uncomment the next line)
        data_transformed = city.data[:1500]

        #data_transformed = city.data.drop_duplicates(subset=[column_name_description])
        data_transformed = self.lowercase_text(data_transformed, column_name_description)
        data_transformed = self.undecode_text(data_transformed, column_name_description)
        
        ids_locations = Locator().search_all_locations(data_transformed, column_name_id, column_name_description, city.statistics, city.name)

        city.ids_locations = ids_locations
        city.column_name_id = column_name_id

        log.info(f'TRANSFORM {city.name} -- SUCCESSFULLY FINISHED - IDs Locations: {len(ids_locations)}')

    

    def lowercase_text(self, dataFrame: pd.DataFrame, column: str):

        log.debug("Starting lowercase text...")
    
        for index, row in dataFrame.iterrows():
            dataFrame.loc[index, column] = row[column].lower()
        
        log.debug("...Lowercase finished successfully !!")
        return dataFrame

    

    def undecode_text(self, dataFrame: pd.DataFrame, column: str) -> pd.DataFrame:

        log.debug("Starting undecode text...")
    
        for index, row in dataFrame.iterrows():
            dataFrame.loc[index, column] = unidecode(row[column])
        
        log.debug("...Undecode finished successfully !!")
        return dataFrame

