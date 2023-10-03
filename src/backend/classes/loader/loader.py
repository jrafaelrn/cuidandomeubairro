import logging
import datetime


from tqdm import tqdm
from classes.db import DB

log = logging.getLogger(__name__)


class Loader:    
    
    def load(self, city):

        self.city = city
        self.data = city.data

        log.info('Starting load...')
        print('Starting load...')
        
        self.database = DB()
        self.load_data()
        self.load_metadata()

        log.info('LOAD -- SUCCESSFULLY FINISHED')
        print('LOAD -- SUCCESSFULLY FINISHED')



    def load_data(self):

        progress_bar_bd = tqdm(total=len(self.data), desc=f'{self.city.name} >>> Database...', position=1, leave=False, mininterval=5)

        # Isolar essa regra futuramente para permitir multiplas cidades
        for index, row in self.data.iterrows():

            progress_bar_bd.update(1)

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
        
        progress_bar_bd.close()



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
            location = self.city.ids_locations[row[self.city.column_name_id]]

            # Add the location to the columns
            if location:
                columns_name.append('latitude')
                columns_name.append('longitude')

                columns_value.append(location.latitude)
                columns_value.append(location.longitude)
                
        except:
            #print(f'WARN - Location not found for id: {row[self.column_name_id]}')    
            pass


    def load_metadata(self):
        self.database.update_metadata()
