import os
import sys
import datetime
import logging as log
import timeit

from tools.telegram import Telegram
from importlib import import_module

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(APP_DIR))

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
        message = f'Error running file: {file} \n--> {e}'
        log.error(message.replace('\n', ' '))
        telegram.sendMessage(message)



#################################
#   Everything starts here...   #
#################################

if __name__ == '__main__':
    
    # Configure log level, format and file
    configure_logs()
    
    message = f'Starting ETL at: {datetime.datetime.now().strftime("%H:%M:%S")}'
    log.info(message)
    telegram.sendMessage(message)
    
    
    # Run every Python file in the scripts folder and measure the time
    total_time = timeit.timeit(execute_scripts, globals=globals(), number=1)
    
    
    message = f'Finished ETL at: {datetime.datetime.now().strftime("%H:%M:%S")} \nTotal time: {total_time}'
    log.info(message.replace('\n', ' '))
    telegram.sendMessage(message)
