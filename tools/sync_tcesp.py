import requests
import zipfile
import datetime
import os

from tqdm import tqdm
from slice_tce_dateset import *


def download_data(url: str, filename: str):
    
    print(f"Downloading {url}...")
    
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
        print("ERROR, something went wrong")
    else:
        print(f"Downloaded {filename} successfully")
        
        
                
def unzip_data(filename: str, destination: str):
    
    print(f"Unzipping {filename}... to {destination}")
    
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(destination)
        
        
def clear_temp_files():
    
    print("Clearing temp files...")
    os.remove('./original_data/despesas-2022.zip')
    os.remove('./original_data/despesas-2022.csv')
    
    

if __name__ == '__main__':
    
    print(f"Starting SYNC at {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    urls = ['https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2022.zip']
    
    for url in urls:
        file_name = url.split('/')[-1]
        download_data(url, f'original_data/{file_name}')        
        unzip_data(f'original_data/{file_name}', 'original_data/')
        
    # from slice_tce_dateset.py
    run() 
        
    # Clear temp files
    clear_temp_files()
        