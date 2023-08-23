import os

def clear_temp_files(data_temp_folder: str):
    
    print("Clearing temp files...")
    
    for folder in os.listdir(data_temp_folder):
        
        if folder == 'log':
            continue
        
        folder_path = os.path.join(data_temp_folder, folder)
        
        try:
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                os.remove(file_path)
            
            os.rmdir(folder_path)
        except Exception as e:
            print(e)
    