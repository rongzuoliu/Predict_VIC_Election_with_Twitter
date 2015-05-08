__author__ = 'rongzuoliu'

from geopy.geocoders import Nominatim


geolocator = Nominatim()
location = geolocator.geocode("800 swanston street, vic", timeout=10)
print(location.address)
print((location.latitude, location.longitude))

# (40.7410861, -73.9896297241625)
# print(location.raw)
# {'place_id': '9167009604', 'type': 'attraction', ...}