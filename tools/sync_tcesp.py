import requests
import zipfile

from slice_tce_dateset import *

def download_data(url: str, filename: str):
    req = requests.get(url)
    
    with open(filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                
                
def unzip_data(filename: str):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall('./original_data')
        
        


if __name__ == '__main__':
    
    urls = ['https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2022.zip']
    
    for url in urls:
        file_name = url.split('/')[-1]
        download_data(url, file_name)        
        unzip_data(file_name)
        
        # from slice_tce_dateset.py
        run() 