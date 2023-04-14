class City:
    
    def __init__(self, name):
        self.name = name
        self.terms = {}
        
        
    def update_term(self, term):
        self.terms[term] = self.terms.get(term, 0) + 1
        
    
    def to_dict(self):
        return {self.name: self.terms}
    
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    
    def __str__(self) -> str:
        return self.name