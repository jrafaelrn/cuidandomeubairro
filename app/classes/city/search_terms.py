import re
import logging

log = logging.getLogger(__name__)


def search_all_terms(TERMS_CONTENT, line: str):

    #console.debug(f'Searching line: {line}...')
    results = []

    for regex in TERMS_CONTENT:
        
        position = re.search(regex, line, re.IGNORECASE)
        
        if position:
            result = {}
            result['term'] = regex
            result['position'] = position.start()
            results.append(result)
    
    
    return results
