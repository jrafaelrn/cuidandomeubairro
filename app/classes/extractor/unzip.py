import zipfile
                
def unzip_data(filename: str, destination: str):
    
    print(f"Unzipping {filename}... to {destination}")
    
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(destination)
        