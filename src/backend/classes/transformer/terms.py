import os
import logging
from unidecode import unidecode

log = logging.getLogger(__name__)


class Terms:

    def __init__(self):
        self.FILE_PATH = os.path.abspath(__file__)
        self.FOLDER_PATH = os.path.dirname(self.FILE_PATH)

    
    def load_terms(self):

        terms_file = os.path.join(self.FOLDER_PATH, "terms.txt")
        terms_content = None

        with open(terms_file, 'r', encoding="utf-8") as f:
            terms_content = f.read().splitlines()
            terms_content = [term.lower() for term in terms_content]
            terms_content = [unidecode(term) for term in terms_content]
            log.debug(f'Loaded {len(terms_content)} terms: {terms_content}')

        return terms_content