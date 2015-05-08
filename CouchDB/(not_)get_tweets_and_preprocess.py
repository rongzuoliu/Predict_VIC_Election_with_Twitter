__author__ = 'rongzuoliu'
# coding=utf-8

import couchdb
import time
import re
from geopy.geocoders import Nominatim
import json
from shapely.geometry import shape, Point


def map_reduce(dbname, search_term):
    s_time = time.time()
    server = couchdb.Server()
    db = server[dbname]

    wf = open("t_" + dbname + "_" + search_term + ".txt", 'w')
    wf.write('UserID;;;;;;;;TweetID;;;;;;;;Text;;;;;;;;CreatedAt;;;;;;;;Location;;;;;;;;Lat;;;;;;;;Lon;;;;;;;;Electorate\n\n')

    # todo: error!!!!!!!!
    # todo: if GeoLocation / place does not exist, can't map reduce
    map_fun = '''
    function(doc) {
      if (doc.text.search(/''' + search_term + '''/) != -1) {
        emit(doc.id, {UserID: doc.user.id, TweetID: doc.id, GeoLocation: doc.geoLocation, Place: doc.place, Location: doc.user.location, Text: doc.text, CreatedAt: doc.createdAt});
      }
    }'''

    UserID = 0
    TweetID = 0
    GeoLocation = ''
    Place = ''
    Location = ''
    Text = ''
    CreatedAt = ''
    Lat = 200.00 # invalid lat
    Lon = 200.00 # invalid lon
    Electorate = ''

    print '\nstart to map reduce...........'
    print 'searching: %s in database: %s............' %(search_term, dbname)

    for row in db.query(map_fun):
        # print '/n', row
        TweetID = row.value.get('TweetID')
        UserID = row.value.get('UserID')
        GeoLocation = row.value.get('GeoLocation').encode('utf-8')
        Place = row.view.get('Place').encode('utf-8')
        Text = re.sub(r'\n', ' ', row.value.get('Text').encode('utf-8'))
        CreatedAt = re.sub(r'\n', '', row.value.get('CreatedAt').encode('utf-8'))

        Location = re.sub(r'\n', ' ', row.value.get('Location').encode('utf-8'))
        (Lat, Lon) = get_geocode(Location)
        Electorate = belong_to_electorate(Lat, Lon).encode('utf-8')

        wf.write("%s;;;;;;;;%s;;;;;;;;%s;;;;;;;;%s;;;;;;;;%s;;;;;;;;%s;;;;;;;;%s;;;;;;;;%s\n"
                 %(UserID, TweetID, Text, CreatedAt, Location, Lat, Lon, Electorate))

    e_time = time.time()
    last_time = e_time - s_time
    wf.write('\n\nMap reduce used time: %ss \n' % last_time)
    wf.close()


# todo: deal with the situation when location is already a lat and lon
def get_geocode(address):
    lat = 200.00 # initiate with an invalid lat
    lon = 200.00 # initiate with an invalid lon

    if (address): # address is valid
        has_mel = re.findall(r'melbourne', address.lower(), 0)
        has_vic = re.findall(r'victoria', address.lower(), 0)
        has_aus = re.findall(r'australia', address.lower(), 0)
        addr = re.sub('melbourne','', address.lower()) # if address contain 'melbourne'
        addr = re.sub('victoria','', addr.lower()) # if address contain 'victorian'
        addr = re.sub('australia','', addr.lower()) # if address contain 'australia'
        print "addr is %s" % addr

        # the most common situation:
        # address is a rough address which only contains "melbourne", "victorian" or "australia"
        # to save time: directly assign the lat and lon of Melbourne's to this tweet
        if (not(re.findall(r'\w', addr, 0))):
            lat = -37.8602828 # lat of Melboure
            lon = 145.079616

        # address is a specific address
        else:
            if (not(has_vic and has_aus)):
                # still try to look for a place in VIC, AUS
                address = address + ", VIC, Australia" # make sure the geocode will look for a place in VIC
            print "address is %s" % address
            geo_locator = Nominatim()
            geocode = geo_locator.geocode(address, timeout=50)
            print "Geocode is: %s" % geocode
            if (geocode):
                lat = geocode.latitude
                lon = geocode.longitude
    return (lat, lon)


def belong_to_electorate(lat, lon):

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
                electorate = feature['properties'].get('Name')

    print 'Belong to Electorate: ', electorate
    return electorate

