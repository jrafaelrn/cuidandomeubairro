import requests
import logging

# Progress bar
from tqdm import tqdm

# Logging configuration
log = logging.getLogger(__name__)


def download_file_from_url(url: str, filename: str):
    
    log.info(f"Downloading [{url}] to [{filename}]")
    
    req = requests.get(url, stream=True)
    total_size_bytes = int(req.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_bytes, unit='iB', unit_scale=True)
    
    with open(filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=block_size):
            progress_bar.update(len(chunk))            
            f.write(chunk)
    
    progress_bar.close()
    if total_size_bytes != 0 and progress_bar.n != total_size_bytes:
        log.error("ERROR, something went wrong")
    else:
        log.info(f"Downloaded {filename} successfully")