import os
import sys
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from dotenv import load_dotenv
from tools.telegram import Telegram


telegram = Telegram()

def log_and_telegram(message):
    global telegram
    print(message)
    telegram.sendMessage(message)



if __name__ == '__main__':
    
    load_dotenv()
    
    log_and_telegram(f"Starting ETL at: {datetime.datetime.now().strftime('%H:%M:%S')}")

    # Loop through the files and run the 'run' method on each one
    scripts_folder = f'{SCRIPT_DIR}/scripts'
    for file in os.listdir(scripts_folder):
        if file.endswith('.py'):
            print(f'Running file: {file}')
            os.system(f'python {scripts_folder}/{file}')