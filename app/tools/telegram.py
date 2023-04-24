import os
import requests

from dotenv import load_dotenv

class Telegram(object):

    
    def __init__(self):
        
        load_dotenv()

        self.TELEGRAM_API_KEY = self.get_api_key()
        self.TELEGRAM_CHAT_ID = self.get_chat_id()

        if self.TELEGRAM_API_KEY is None or self.TELEGRAM_CHAT_ID is None:
            return            

        url_base = 'https://api.telegram.org/bot'
        self.url_base = f'{url_base}{self.TELEGRAM_API_KEY}/'

    
    def get_api_key(self):        
        try:
            return os.environ['TELEGRAM_API_KEY']
        except Exception as e:
            print(f'Error - Get KEY from environment: {e}')    
            return None
        
    def get_chat_id(self):
        try:
            return os.environ['TELEGRAM_CHAT_ID']
        except Exception as e:
            print(f'Error - Get CHAT ID from environment: {e}')    
            return None

    


    def sendMessage(self, content: str):

        print(f'<<--- Sending message by Telegram: [{content}] -- to chat: {self.TELEGRAM_CHAT_ID}')
        link_resp = f'{self.url_base}sendMessage?chat_id={self.TELEGRAM_CHAT_ID}&text={content}'
        
        resp = requests.get(link_resp)
        #print(f'\t<<--- Send message - Response: {resp.status_code} - {resp.text}')
        
        if resp.status_code == 200:
            print("OK - Message sent")
        else:
            print("Error - Message not sent")



    def print_updates(self):
        
        link_req = f'{self.url_base}getUpdates'
        resp = requests.get(link_req)
        print(f'<<--- Get updates - Response: {resp.status_code} - {resp.text}')