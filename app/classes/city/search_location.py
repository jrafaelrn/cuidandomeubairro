from geopy.geocoders import Nominatim

geolocator = Nominatim(domain='localhost:8088', scheme='http')
#geolocator = Nominatim(user_agent="cmb3.0")

def search_local(location: str):
    
    #print(f'Searching location: {location}...')
    location = geolocator.geocode(location, timeout=10)
    #print(f'\tReturn Location: {location}...')
    if not location:
        return None
    
    return location
    