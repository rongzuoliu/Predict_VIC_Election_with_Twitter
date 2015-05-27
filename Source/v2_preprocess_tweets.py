__author__ = 'rongzuoliu'
# coding=utf-8

import re
import json
import couchdb
from shapely.geometry import shape, Point
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

#import source files
from ElectoratesInfo import electoratesInfo



def tag_electorate(db, doc):

    latitude = 200.00 # Initiate with invalid value
    longitude = 200.00 # Initiate with invalid value
    electorate = '' # Initiate with invalid value

    # Way 1: get lat/lon from 'geoLocation' field, then use lat/lon to tag electorate
    if ('geoLocation' in doc):
        print 'use way1'
        geolocation = doc['geoLocation']
        latitude = geolocation['latitude']
        longitude = geolocation['longitude']
        electorate = determine_electorate(latitude, longitude)

    # Way 2: get lat/lon from 'place' field, then use lat/lon to tag electorate
    elif ('place' in doc):
        if ('boundingBoxCoordinates' in doc):
            print 'use way2'
            latitude = doc['place']['boundingBoxCoordinates'][0][0]['latitude']
            longitude = doc['place']['boundingBoxCoordinates'][0][0]['longitude']
            electorate = determine_electorate(latitude, longitude)

    # Way 3 and 4: get lat/lon through 'location' field
    elif ('location' in doc['user']):
        location = doc['user']['location']
        print location
        if (location != None):

            # Way 3: electorate name (except 'Melbourne', since it's very common)appears in 'location'
            for eInfo in electoratesInfo:
                if (re.findall(eInfo[0].lower(), location.lower(), 0) and not(re.findall("Melbourne".lower(), location.lower(), 0))):
                    print 'use way3'
                    electorate = eInfo[0] # assign electorate name
                    (latitude, longitude) = geocoding(electorate)
                    break

            # Way 4: more general situation, get lat/lon via Geocoding
            if (electorate == '' or latitude == 200.00 or longitude == 200.00):
                print 'use way4'
                (latitude, longitude) = geocoding(location)
                electorate = determine_electorate(latitude, longitude)

    print "latitude: %s; longitude: %s;    belong to electorate: %s\n" % (latitude, longitude, electorate)
    doc['electorate'] = electorate
    db.save(doc)



# todo: deal with the situation when location is already a lat and lon
def geocoding(address):
    lat = 200.00 # Initiate with an invalid value
    lon = 200.00 # Initiate with an invalid value

    if (address):
        print address
        has_mel = re.findall(r'melbourne', address.lower(), 0)
        has_vic = re.findall(r'victoria', address.lower(), 0) or re.findall(r'VIC', address, 0)
        has_aus = re.findall(r'australia', address.lower(), 0) or re.findall(r'Aus', address, 0)

        print has_mel
        print has_vic
        print has_aus

        addr = re.sub(r'(melbourne,victoria,australia)', '', address.lower())
        addr = re.sub(r'(VIC,Vic,AUS,Aus)', '', addr) # delete 'VIC', 'Vic', 'Aus', 'AUS' in address
        print "addr is %s" % addr

        # the most common situation:
        # address is a rough address which only contains "melbourne", "victorian" or "australia"
        # to save time: directly assign the values as lat/lon of 'Melbourne'
        if (not(re.findall(r'\w', addr, 0))):
            lat = -37.8602828 # lat of Melboure
            lon = 145.079616 # lon of Melboure

        # address is a specific address
        else:
            if (not(has_vic and has_aus)):
                # still try to look for a place in VIC, AUS
                address = address + ", VIC, Australia" # make sure the geocode will look for a place in VIC
            # print "address is %s" % address
            geo_locator = Nominatim()
            try:
                geocode = geo_locator.geocode(address, timeout=40)
                print "Queried '%s', the geocode result is: %s" % (address, geocode)
                if (geocode):
                    lat = geocode.latitude
                    lon = geocode.longitude
                else:
                    "Queried geocode result is: null"
            except (GeocoderTimedOut) as e:
                print "Exception: %s" % e

        print "lat is %s; lon is %s" % (lat, lon)
    return (lat, lon)



def determine_electorate(lat, lon):
    electorate = 'null'
    # deal with the most common situation: the location is melbourne
    if (lat==-37.8602828 and lon==145.079616):
        electorate = "Melbourne"
    else:
        # load GeoJSON file containing sectors
        with open('../DataSource/electorateFeatures.json') as f:
            js = json.load(f)

        # construct point based on lat/long returned by geocode
        point = Point(lon, lat)

        # check each polygon to see if it contains the point
        for feature in js['features']:
            polygon = shape(feature['geometry'])
            # print polygon.bounds
            if polygon.contains(point):
                electorate = feature['properties']['Name']

    print 'Belong to Electorate: ', electorate
    return electorate



def tag_textTo(db, doc):
    parties = ['Labor', 'Liberal', 'Greens', 'Nationals']
    leaders = ['Daniel Andrews', 'Denis', 'Napthine']
    to_party = []
    to_leader = []
    if ('text' in doc):
        for party in parties:
            # print party
            find_party = re.findall(party, doc['text'], 0)
            if (find_party):
                for p in find_party:
                    if (not (p in to_party)):
                        to_party.append(p)
        for leader in leaders:
            find_leader = re.findall(leader, doc['text'], 0)
            if (find_leader):
                for l in find_leader:
                    if (not (l in to_leader)):
                        to_leader.append(l)

        # todo: to check whether 'textTo' is already exist
        doc['textTo'] = {'toParty': to_party, 'toLeader': to_leader}
        print doc['textTo']
        print '\n'
        db.save(doc)



def main():
    server = couchdb.Server('http://127.0.0.1:5984/')
    db = server['vic_election']

    for id in db:
        doc = db.get(id)
        tag_textTo(db, doc)

    for id in db:
        doc = db.get(id)
        if ('electorate' not in doc):
            tag_electorate(db, doc)


if __name__ == "__main__":

    main()









