import os
import requests
import logging

from dotenv import load_dotenv

log = logging.getLogger(__name__)


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
            log.error(f'Error - Get KEY from environment: {e}')    
            return None
        
    def get_chat_id(self):
        try:
            return os.environ['TELEGRAM_CHAT_ID']
        except Exception as e:
            log.error(f'Error - Get CHAT ID from environment: {e}')    
            return None

    


    def sendMessage(self, content: str):

        log.debug(f'<<--- Sending message by Telegram: [{content}] -- to chat: {self.TELEGRAM_CHAT_ID}'.replace('\n', ' '))
        link_resp = f'{self.url_base}sendMessage?chat_id={self.TELEGRAM_CHAT_ID}&text={content}'
        
        resp = requests.get(link_resp)
        #log.debug(f'\t<<--- Send message - Response: {resp.status_code} - {resp.text}')
        
        if resp.status_code == 200:
            log.debug("OK - Message sent")
        else:
            log.error("Error - Message not sent")



    def print_updates(self):
        
        link_req = f'{self.url_base}getUpdates'
        resp = requests.get(link_req)
        log.debug(f'<<--- Get updates - Response: {resp.status_code} - {resp.text}')