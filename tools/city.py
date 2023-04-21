class City:
    
    def __init__(self, name: str, code: str):
        self.name = name
        self.terms = {}
        self.total_rows = 0
        self.code = code
        
        
    def update_term(self, term):
        self.terms[term] = self.terms.get(term, 0) + 1
        
    def terms_statistics_to_dict(self):
        self.terms['total_rows'] = self.total_rows
        self.terms['cod_cidade'] = self.code
        return self.terms
    
    
    def set_total_rows(self, total_rows):
        self.total_rows = total_rows
        
        
    # File Path
    def set_file_path(self, file_path):
        self.file_path = file_path
        
    def get_file_path(self):
        return self.file_path
    
    
    def get_file_name(self):
        # Get name from full path and remove the extension
        file_name = self.file_path.split('/')[-1]
        file_extension = file_name.split('.')[-1]
        return file_name.replace(f'.{file_extension}', '')
    
    
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    
    def __str__(self) -> str:
        return self.name