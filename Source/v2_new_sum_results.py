__author__ = 'rongzuoliu'

import copy
import re
import json
import os
import couchdb


# todo: separate parites into a file


# initialisation
parties = ['Labor', 'Liberal', 'Greens', 'Nationals']
counts = {'pos': 0, 'neu': 0, 'neg': 0, 'total': 0}
party_counts = {}
for party in parties:
    party_counts[party] = copy.deepcopy(counts)
elect_counts = {}
elect_counts['name'] = ''
elect_counts['parties'] = copy.deepcopy(party_counts)
total_counts = []

# todo: change the electorateFeatures.json to ElectoratesInfo.py
with open('../DataSource/electorateFeatures.json') as f:
    js_old = json.load(f)
    # each feature contains the whole information about an electorate
    for feature in js_old['features']:
        name = feature['properties'].get('Name')
        elect_counts['name'] = name
        elect_counts['parties'] = copy.deepcopy(party_counts)
        total_counts.append({'electorate': copy.deepcopy(elect_counts)})
    print total_counts



############################function definitions###########################################


def sum_prediction(doc):

    if 'sentiment' in doc and 'electorate' in doc and 'towards' in doc:
        sentiment = doc['sentiment']
        electorate = doc['electorate']
        towards = doc['towards']
        print sentiment['sentiment']
        print electorate
        print towards

        for elect in total_counts:
            if elect['electorate']['name'] == electorate: # This tweet is belong to this electorate
                # print elect
                party = towards # This tweet is towards to this party
                # print party
                if (sentiment['sentiment'] == 'pos'):
                    elect['electorate']['parties'][party]['pos'] += 1
                elif (sentiment['sentiment'] == 'neu'):
                    elect['electorate']['parties'][party]['neu'] += 1
                elif (sentiment['sentiment'] == 'neg'):
                    elect['electorate']['parties'][party]['neg'] += 1
                # sum up the total sentiment result for this party in this electorate
                elect['electorate']['parties'][party]['total'] += 1
            else: # This tweet isn't belong to any of these electorates
                pass # todo: when tweet isn't belong to any electorates


def main():

    total = 0.0 # for division
    server = couchdb.Server('http://127.0.0.1:5984/')
    # db = server['vic_election']
    db = server['test_towards']

    for id in db:
        doc = db.get(id)
        sum_prediction(doc)
        total += 1
    print total
    print total_counts


    # wf = open('electData.js', 'w')
    # wf.write("var electData = {\n\"type\": \"Counts of Predicted Election Results \",\n\"counts\": [\n")
    #
    # i = 0
    # for elect in total_counts:
    #     js = json.dumps(elect, ensure_ascii=False)
    #     if i < len(total_counts)-1:
    #         wf.write(js.encode('utf-8') + ',\n')
    #         i += 1
    #     else:
    #         wf.write(js.encode('utf-8') + '\n')
    #
    # wf.write("]};")
    # wf.close()




if __name__ == '__main__':
    main()
