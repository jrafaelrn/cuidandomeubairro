import zipfile
import logging


log = logging.getLogger(__name__)
                
def unzip_data(filename: str, destination: str):
    
    log.info(f"Unzipping [{filename}] to [{destination}]")
    
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(destination)
        