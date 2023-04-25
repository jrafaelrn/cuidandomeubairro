import os
import sys
import datetime
import logging as log

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(APP_DIR))

from tools.telegram import Telegram
from importlib import import_module


telegram = Telegram()   



def configure_logs():
    log.basicConfig(
        level=log.DEBUG,
        format='%(asctime)s;%(name)s;%(levelname)s;%(message)s',
        filename=f'{APP_DIR}/data_temp/logs/run_etl_cmb.log',
        filemode='a'
    )



def execute_scripts():
    
    # Add the scripts folder to the path environment
    scripts_folder = f'{APP_DIR}/scripts'
    sys.path.append(scripts_folder)
    
    # Loop through the files and run Python files
    for file in os.listdir(scripts_folder):
        if file.endswith('.py'):
            execute(file)
            


# Try execute method 'run' from the file
def execute(file):
    
    log.info(f'Running file: {file}')
    module = import_module(file.replace('.py', ''))
    
    try:
        module.run()
    
        message = f'Finished successfully: {file}' 
        log.info(message)
        telegram.sendMessage(message)
    
    except Exception as e:
        message = f'Error running file: {file} --> {e}'
        log.error(message)
        telegram.sendMessage(message)



#################################
#   Everything starts here...   #
#################################

if __name__ == '__main__':
    
    # Configure log level, format and file
    configure_logs()
    
    telegram.sendMessage(f"Starting ETL at: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    # Run every Python file in the scripts folder
    execute_scripts()
    
    telegram.sendMessage(f"Finished ETL at: {datetime.datetime.now().strftime('%H:%M:%S')}")
