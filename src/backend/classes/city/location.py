
'''
original_description = "obra inaugural na praca vereador xyz 2569 - Bairro ABC"
[
    {
        "search_term": "obra inaugural na praca vereador xyz",
        "variation": -1,
        "positions": {
            latitude: 123.123,
            longitude: 123.123,
        },
    }
    {
        "search_term": "praca vereador xyz",
        "variation": 2,
        "locations": {
            latitude: 123.456,
            longitude: 123.456,        
        }
    },
    {
        "search_term": "praca vereador xyz 2569 - Bairro ABC",
        "variation": 6,
        "locations": {
            latitude: 123.456,        
            latitude: 123.456,
        }
    }
]
'''
class Location:
    
    def __init__(self, original_description: str) -> None:
        self.original_description = original_description
        self.searchs = []
        
        
    def add_search(self, search_term: str, variation: int, locations: list):
        
        search = {}
        search['search_term'] = search_term
        search['variation'] = variation
        search['locations'] = locations
        self.searchs.append(search)
        
   