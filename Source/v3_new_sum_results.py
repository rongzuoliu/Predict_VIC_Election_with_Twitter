__author__ = 'rongzuoliu'

import copy
import json
import couchdb

from ElectoratesInfo import ELECTINFO
from PolitClassification import PARTIES, LEADERS, PARTYANDLEADER


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


def try_to_count_in(doc):
    if_count = False
    # todo: change 'sentiment' to 'attitude'
    if 'sentiment' in doc and 'electorate' in doc and 'towards' in doc:
        attitude = doc['sentiment']
        sentiment = doc['sentiment']['sentiment']
        electorate = doc['electorate']
        towards = doc['towards']
        # print attitude['sentiment']
        # print electorate
        # print towards
        if sentiment and towards and electorate:
            for elect, count in elect_counts.iteritems():
                if elect == electorate: # This tweet is belong to this electorate
                    party = towards # This tweet is towards to this party
                    count[party][sentiment] += 1
                    count[party]['total'] += 1
                    if_count = True
                else: # This tweet isn't belong to any of these electorates
                    pass # todo: when tweet isn't belong to any electorates
    return if_count


def archive_to_js(total):
    wf = open('electDataCounts.js', 'w')
    wf.write('var electData = {\n\"type\": \"Counts of Predicted Election Results \",\n\"totalCount\": \"' + str(total) +'\",\n"counts\": [\n"')

    i = 0
    for elect, count in elect_counts.iteritems():
        js = json.dumps({elect: count}, ensure_ascii=False)
        if i < len(elect_counts)-1:
            wf.write(js.encode('utf-8') + ',\n')
            i += 1
        else:
            wf.write(js.encode('utf-8') + '\n')

    wf.write("]};")
    wf.close()



def main():

    total = 0
    server = couchdb.Server('http://127.0.0.1:5984/')
    # db = server['vic_election']
    db = server['test_towards']

    for id in db:
        doc = db.get(id)
        if try_to_count_in(doc):
            total += 1
    print total
    print elect_counts

    archive_to_js(total)

if __name__ == '__main__':
    main()
