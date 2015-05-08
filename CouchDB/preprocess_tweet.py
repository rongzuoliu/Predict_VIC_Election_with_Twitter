__author__ = 'rongzuoliu'
# coding=utf-8

import time
import re
import os
from geopy.geocoders import Nominatim
import json
from shapely.geometry import shape, Point
from itertools import islice

#json format:
# {UserID: doc.user.id, TweetID: doc.id,
# GeoLocation: doc.geoLocation, Place: doc.place, Location: doc.user.location,
# Text: doc.text, CreatedAt: doc.createdAt}

# todo: assign value to 'towards' field

def proprocess_tweet(r_path):

    temp = re.sub('.+_.+_', '', r_path, 0)
    term = re.sub('.txt', '', temp, 0)
    print "search term is: %s" % term
    towards = term

    s_time = time.time()
    w_path = re.sub('.+raw_', '../ProprocessedTweets/geoed_', r_path)
    wf = open(w_path, 'w')

    latitude = 200.00 # invalid lat
    longitude = 200.00 # invalid lon
    location = ''
    electorate = ''

    with open(r_path) as file:
        for line in file:
            # if (line)

            js_old = json.loads(line)

            # Firstly: get geocode of the tweet

            # Way 1: get lat/lon directly from the lat/lon fields of the tweet if they are available
            if ('geoLocation' in js_old):
                latitude = js_old['geoLocation']['latitude']
                longitude = js_old['geoLocation']['longitude']
                belong_to_electorate(latitude, longitude)

            # Way 2: get lat/lon from the place field of the tweet if it's available
            elif ('place' in js_old):
                if (js_old['place'].has_key('boundingBoxCoordinates')):
                    latitude = js_old['place']['boundingBoxCoordinates'][0][0].get('latitude')
                    longitude = js_old['place']['boundingBoxCoordinates'][0][0].get('longitude')

            # Way 3: get lat/lon through querying geocode based on the location field of the tweet if they are available
            else:
                location = js_old['location']
                (latitude, longitude) = get_geocode_via_location(location)


            # Secondly: get electorate of the tweet
            electorate = belong_to_electorate(latitude, longitude)

            print "latitude: %s; longitude: %s; belong to electorate: %s\n" % (latitude, longitude, electorate)

            js_old['latitude'] = latitude
            js_old['longitude'] = longitude
            js_old['electorate'] = electorate

            js_old['towards'] = towards

            js_new = json.dumps(js_old, ensure_ascii=False)
            wf.write(js_new.encode('utf-8') + '\n')
    wf.close()
    e_time = time.time()
    last_time = e_time - s_time
    print '\nUse time: %s \n' % last_time
    print '\nResult is stored in %s \n' % w_path





# todo: deal with the situation when location is already a lat and lon
def get_geocode_via_location(address):
    lat = 200.00 # initiate with an invalid lat
    lon = 200.00 # initiate with an invalid lon

    if (address): # address is valid
        has_mel = re.findall(r'melbourne', address.lower(), 0)
        has_vic = re.findall(r'victoria', address.lower(), 0)
        has_aus = re.findall(r'australia', address.lower(), 0)
        addr = re.sub('melbourne','', address.lower()) # if address contain 'melbourne'
        addr = re.sub('victoria','', addr.lower()) # if address contain 'victorian'
        addr = re.sub('australia','', addr.lower()) # if address contain 'australia'
        # print "addr is %s" % addr

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
            # print "address is %s" % address
            geo_locator = Nominatim()
            geocode = geo_locator.geocode(address, timeout=50)
            print "Queried geocode result is: %s" % geocode
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




if __name__ == "__main__":

    r_path = []
    direct_path = "../RawTweets"
    for file in os.listdir(direct_path):
        if file.endswith(".txt"):
            r_path.append(direct_path + '/' + file)

    for file_path in r_path:
        proprocess_tweet(file_path)
    # r_path = "../RawTweets/raw_tweets2010_Daniel Andrews.txt"
    r_path = "../RawTweets/raw_tweets2010_Greens.txt"
    proprocess_tweet(r_path)
