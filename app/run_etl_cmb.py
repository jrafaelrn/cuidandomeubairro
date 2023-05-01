import os
import datetime
import logging as log
import timeit
import sys
import cProfile

from tools.telegram import Telegram
from tools.human_readable import convert_seconds_to_human_readable
from config import configure_paths
from importlib import import_module

APP_FILE_PATH = os.path.abspath(__file__)
APP_FOLDER_PATH = os.path.dirname(APP_FILE_PATH)

telegram = Telegram()   


def configure_logs():
    log.basicConfig(
        level=log.DEBUG,
        format='%(asctime)s;%(name)s;%(levelname)s;%(message)s',
        filename=f'{APP_FOLDER_PATH}/data_temp/logs/run_etl_cmb.log',
        filemode='w'
    )




def execute_scripts():
    
    scripts_folder = f'{APP_FOLDER_PATH}/scripts'
    
    # Loop through the files and run Python files
    for file in os.listdir(scripts_folder):
        if file.endswith('.py'):
            execute(file)
            


# Try execute method 'run' from the file
def execute(file):
    
    log.info(f'Running file: {file}')
    file = file.replace('.py', '')
    module = import_module(file)
    
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
    
    start_time = datetime.datetime.now()
    
    # Configure environment
    configure_paths(APP_FOLDER_PATH)
    configure_logs()
    
    # Log start process and send Telegram
    message = f'Starting ETL at: {datetime.datetime.now().strftime("%H:%M:%S")}'
    log.info(message)
    #telegram.sendMessage(message)
    
    
    # Run every Python file in the scripts folder and measure the time
    #total_time = timeit.timeit(execute_scripts, globals=globals(), number=1)
    cProfile.run('execute_scripts()', sort='cumtime')
    
    # Convert seconds to hh:mm:ss
    end_time = datetime.datetime.now()
    total_time_readable = convert_seconds_to_human_readable((end_time - start_time).total_seconds())
    
    # Log end process and send Telegram    
    message = f'Finished ETL at: {datetime.datetime.now().strftime("%H:%M:%S")} \nTotal time: {total_time_readable}'
    log.info(message.replace('\n', ' '))
    #telegram.sendMessage(message)
