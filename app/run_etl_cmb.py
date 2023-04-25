import os
import sys
import datetime
import logging

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(APP_DIR))

from tools.telegram import Telegram
from importlib import import_module


telegram = Telegram()   


def configure_logs():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s;%(name)s;%(levelname)s;%(message)s',
        filename=f'{APP_DIR}/data_temp/logs/run_etl_cmb.log',
        filemode='a'
    )


def execute_scripts():
    
    # Loop through the files and run the 'run' method on each one
    scripts_folder = f'{APP_DIR}/scripts'
    sys.path.append(scripts_folder)
    
    for file in os.listdir(scripts_folder):
        if file.endswith('.py'):
            execute(file)
            
            
def execute(file):
    
    print(f'Running file: {file}')
    module = import_module(file.replace('.py', ''))
    
    try:
        module.run()
        telegram.sendMessage(f'Finished successfully: {file}')
    except Exception as e:
        telegram.sendMessage(f'Error running file: {file} --> {e}')





if __name__ == '__main__':
    
    configure_logs()
    
    telegram.sendMessage(f"Starting ETL at: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    execute_scripts()
    
    telegram.sendMessage(f"Finished ETL at: {datetime.datetime.now().strftime('%H:%M:%S')}")
