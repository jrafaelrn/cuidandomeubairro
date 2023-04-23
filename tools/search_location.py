from geopy.geocoders import Nominatim

geolocator = Nominatim(domain='localhost:8088/', scheme='http')


def search_local(location: str):
    
    location = geolocator.geocode(query=location, timeout=600)
    
    if not location:
        return None
    
    return location
    