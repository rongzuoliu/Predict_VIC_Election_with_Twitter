__author__ = 'rongzuoliu'

import copy
import re
import json
import couchdb

from ElectoratesInfo import ELECTINFO
from PolitClassification import PARTIES, LEADERS, PARTYANDLEADER

# todo: separate parites into a file

# initialisation
counts = {'pos': 0, 'neu': 0, 'neg': 0, 'total': 0}
party_counts = {}
for party in PARTIES:
    party_counts[party] = copy.deepcopy(counts)
elect_counts = {}
elect_counts['parties'] = copy.deepcopy(party_counts)

for elect_info in ELECTINFO:
    name = elect_info[0]
    elect_counts[name] = copy.deepcopy(party_counts)

print elect_counts
# for key, value in elect_counts.iteritems():
#     print key
#     print value


############################function definitions###########################################


def sum_prediction(doc):

    # todo: change 'sentiment' to 'attitude'
    if 'sentiment' in doc and 'electorate' in doc and 'towards' in doc:
        attitude = doc['sentiment']
        sentiment = doc['sentiment']['sentiment']
        electorate = doc['electorate']
        towards = doc['towards']
        # print attitude['sentiment']
        # print electorate
        # print towards
        for elect, senti in elect_counts.iteritems():
            if elect == electorate: # This tweet is belong to this electorate
                party = towards # This tweet is towards to this party
                senti[party][sentiment] += 1
                senti[party]['total'] += 1
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
    print elect_counts

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
