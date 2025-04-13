#return a search link or reservation link info for restaurants(opentable), movies(Fandango), events(Eventbrite)

import urllib.parse

def generate_opentable_url(restauraunt_name: str) -> str:
    #return an opentable search url for given restaurant
    
    base_url = "https://www.opentable.com/s?term="
    query = urllib.parse.quote(restauraunt_name)
    return base_url + query

def generate_fandango_url(movie_or_theater: str) -> str:
    base_url = "https://www.fandango.com/search?q="
    query = urllib.parse.quote(f"{movie_or_theater}")
    return base_url + query

def generate_eventbrite_url(event_query: str, location: str = "El Paso") -> str:
    
    base_url = "https://www.eventbrite.com/d/tx--el-paso/"
    query = urllib.parse.quote(event_query)
    return base_url + query

