from urllib.request import urlopen
from app import settings
from urllib.parse import urlencode
import json

def geocode(address):
    data = urlencode({
        'address': address,
        'key': settings.GMAPS_SERVERSIDE_API_KEY
    })
    request = urlopen('https://maps.googleapis.com/maps/api/geocode/json?' + data)

    try:
        data = json.load(request)
    except:
        print("geocode json.load error")
        data = None

    return data
    