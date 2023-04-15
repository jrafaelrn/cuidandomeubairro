class City:
    
    def __init__(self, name):
        self.name = name
        self.terms = {}
        self.total_rows = 0
        
        
    def update_term(self, term):
        self.terms[term] = self.terms.get(term, 0) + 1
        
    def set_total_rows(self, total_rows):
        self.total_rows = total_rows
    
    def to_dict(self):
        self.terms['total_rows'] = self.total_rows
        return {self.name: self.terms}
    
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    
    def __str__(self) -> str:
        return self.name