import requests
import logging
import os

# Progress bar
from tqdm import tqdm

# Logging configuration
log = logging.getLogger(__name__)


def download_file_from_url(url: str, filename: str):
    
    message = f"Downloading [{url}] to [{filename}]"
    log.info(message)
    print(message)

    TENTATIVAS_DOWNLOAD = 1
    TIMEOUT_DOWNLOAD = 60 * 15 # 15 minutes

    while TENTATIVAS_DOWNLOAD <= 5:

        try:
    
            clean_files(os.path.dirname(filename))
            
            req = requests.get(url, stream=True, timeout=TIMEOUT_DOWNLOAD)
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
                raise Exception("ERROR, something went wrong - Try {TENTATIVAS_DOWNLOAD}")
            else:
                log.info(f"Downloaded {filename} successfully")
                break
        
        except Exception as e:
            TENTATIVAS_DOWNLOAD += 1
            continue
            
        

def clean_files(folder_path: str):
    for files in os.listdir(folder_path):
        file_path = os.path.join(folder_path, files)
        os.remove(file_path)