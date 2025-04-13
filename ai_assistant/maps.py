#this works in congruence with the chatlogic as well as the resrevations for the ai assistant 
#be able to provide links for maps and reservations in response to user questions like:
#where's L&J Cafe
#or Book me a table at west texas chophouse
#or find me tickets to a mvoie at alamo drafthouse. 
#maps specifically will generate a GMaps URL the user mentions

import urllib.parse

def generate_maps_url(location_name: str) -> str:
    base_url = "https://www.google.com/maps/search/?api=1&query="
    query = urllib.parse.quote(location_name)
    return base_url + query