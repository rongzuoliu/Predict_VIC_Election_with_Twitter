__author__ = 'rongzuoliu'

import json
from shapely.geometry import shape, Point

# load GeoJSON file containing sectors
with open('../DataSource/electorateFeatures.json') as f:
    js = json.load(f)
    # print js


# construct point based on lat/long returned by geocoder
point = Point(-37.810437,144.962953)
xy_point = Point(144.962953,-37.810437)

# check each polygon to see if it contains the point
for feature in js['features']:
    polygon = shape(feature['geometry'])
    # print polygon.bounds
    if polygon.contains(xy_point):
        print 'Found containing polygon:', feature

