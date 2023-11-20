from abc import abstractmethod
import datetime
import logging

from tqdm import tqdm
from classes.db import DB
from classes.city.despesa import Despesa
from dataclasses import fields

log = logging.getLogger(__name__)


class Loader:    
    
    def load(self, city):

        self.city = city
        self.data = city.data

        log.info('Starting load...')
        #print('Starting load...')
        
        self.database = DB()
        self.load_data()
        self.load_metadata()

        log.info('LOAD -- SUCCESSFULLY FINISHED')
        #print('LOAD -- SUCCESSFULLY FINISHED')



    def load_data(self):

        #self.progress_bar_bd = tqdm(total=len(self.data), desc=f'{self.city.name} >>> Database...', position=self.city.level_bar, leave=False, mininterval=5)
        #print(f'2/2 - Loading data for {self.city.name}... - Level: {self.city.level_bar}')
        table_name = "f_despesa"

        for despesa in self.city.despesas:

            #self.progress_bar_bd.update(1)
            
            names, values = self.get_values_from_despesa(despesa)

            self.database.insert(table_name, names, values)
        
        #self.progress_bar_bd.close()




    def get_values_from_despesa(self, despesa):

        names = []
        values = []

        for field in fields(despesa):
            names.append(field.name)
            values.append(getattr(despesa, field.name))            

        return names, values



    def load_metadata(self):

        now = datetime.datetime.now()
        self.database.update_metadata(last_update_cmb=now, last_update_origin=self.city.last_update_origin, origin=self.city.origin)

