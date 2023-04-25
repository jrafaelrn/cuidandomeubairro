import os
import sys
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from tools.telegram import Telegram
from importlib import import_module


telegram = Telegram()


def log_and_telegram(message):
    global telegram
    print(message)
    telegram.sendMessage(message)
    


def execute_scripts():
    
    # Loop through the files and run the 'run' method on each one
    scripts_folder = f'{SCRIPT_DIR}/scripts'
    sys.path.append(scripts_folder)
    
    for file in os.listdir(scripts_folder):
        if file.endswith('.py'):
            module = import_module(file.replace('.py', ''))
            execute(file, module)
            
            
def execute(file, module):
    print(f'Running file: {file}')
    try:
        module.run()
        log_and_telegram(f'Finished successfully: {file}')
    except Exception as e:
        log_and_telegram(f'Error running file: {file} --> {e}')




if __name__ == '__main__':
    log_and_telegram(f"Starting ETL at: {datetime.datetime.now().strftime('%H:%M:%S')}")
    execute_scripts()
    log_and_telegram(f"Finished ETL at: {datetime.datetime.now().strftime('%H:%M:%S')}")
