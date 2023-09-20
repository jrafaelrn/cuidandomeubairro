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
        self.data_transformed = data = data[:250]
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

        log.info('Starting load...')
        print('Starting load...')
        
        self.database = DB()
        self.load_data()
        self.load_metadata()

        log.info('LOAD -- SUCCESSFULLY FINISHED')
        print('LOAD -- SUCCESSFULLY FINISHED')



    def load_data(self):

        # Isolar essa regra futuramente para permitir multiplas cidades
        for index, row in self.data.iterrows():

            table_name = "f_despesa"

            # Formato nomeColunaCSV: nomeColunaDB
            columns = {}
            columns['cd_programa'] = 'cd_programa'
            columns['ds_programa'] = 'ds_programa'
            columns['cd_acao'] = 'cd_acao'
            columns['ds_acao'] = 'ds_acao'
            columns['codigo_municipio_ibge'] = 'cd_municipio'
            columns['id_despesa_detalhe'] = 'id_despesa_detalhe'           
            columns['ds_orgao'] = 'ds_orgao'
            columns['tp_despesa'] = 'tp_despesa'
            columns['nr_empenho'] = 'nr_empenho'
            columns['tp_identificador_despesa'] = 'tp_identificador_despesa'
            columns['nr_identificador_despesa'] = 'nr_identificador_despesa'
            columns['ds_despesa'] = 'ds_despesa'
            columns['dt_emissao_despesa'] = 'dt_emissao_despesa'
            columns['vl_despesa'] = 'vl_despesa'
            columns['ds_funcao_governo'] = 'ds_funcao_governo'
            columns['ds_subfuncao_governo'] = 'ds_subfuncao_governo'
            columns['ds_fonte_recurso'] = 'ds_fonte_recurso'
            columns['ds_cd_aplicacao_fixo'] = 'ds_cd_aplicacao_fixo'
            columns['ds_modalidade_lic'] = 'ds_modalidade_lic'
            columns['ds_elemento'] = 'ds_elemento'
            columns['historico_despesa'] = 'historico_despesa'
            columns['mes_referencia'] = 'mes'
            columns['ano_exercicio'] = 'ano'
            columns['mes_ref_extenso'] = 'mes_extenso'
            
            columns_name = list(columns.values())
            columns_value = self.get_values_from_row(row, columns)

            # Adiciona a localizacao, se existir
            self.get_location_from_row(row, columns_name, columns_value)


            self.database.insert(table_name, columns_name, columns_value)



    def get_values_from_row(self, row, columns: dict) -> list:

        values = []
        
        for column in columns.keys():
            
            value = row[column]
            
            try:                
                
                try:
                    # Try to convert to date
                    new_value = datetime.datetime.strptime(value, '%d/%m/%Y')
                    value = datetime.datetime.strftime(new_value, '%Y/%m/%d')
                except:
                    # Try to convert to float
                    new_value = value.replace(',', '.')
                    new_value = float(new_value)
                    value = new_value

            except:
                pass
            
            values.append(value)

        return values


    def get_location_from_row(self, row, columns_name, columns_value):

        try:
            # Get the location from the row
            location = self.ids_locations[row[self.column_name_id]]

            # Add the location to the columns
            if location:
                
                columns_name.append('localizacao')

                value = f'POINT({location.longitude} {location.latitude})'
                columns_value.append(value)
        except:
            print(f'Location not found for id: {row[self.column_name_id]}')    


    def load_metadata(self):
        self.database.update_metadata()



    #################################################
        
        
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