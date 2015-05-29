__author__ = 'rongzuoliu'

import copy
import json
import couchdb

from ELECTINFO import ELECTINFO
from POLITICLASS import PARTIES


elect_counts = {}
counts = {'pos': 0, 'neu': 0, 'neg': 0, 'total': 0}
party_counts = {}
for party in PARTIES:
    party_counts[party] = copy.deepcopy(counts)
    elect_counts['parties'] = copy.deepcopy(party_counts)
for elect_info in ELECTINFO:
    name = elect_info[0]
    elect_counts[name] = copy.deepcopy(party_counts)

print elect_counts


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


def archive_to_files(total):
    wf_js = open('ELECTDATACOUNTS.js', 'w')
    wf_py = open('ELECTDATACOUNTS.py', 'w')
    wf_js.write('var electData = {\n\"type\": \"Counts of Predicted Election Results \",\n\"totalCount\": \"' + str(total) +'\",\n"counts\": [\n')
    wf_py.write('ELECTDATACOUNTS = {\n\"type\": \"Counts of Predicted Election Results \",\n\"totalCount\": \"' + str(total) +'\",\n"counts\": [\n')

    i = 0
    for elect, count in elect_counts.iteritems():
        js = json.dumps({elect: count}, ensure_ascii=False)
        if i < len(elect_counts)-1:
            wf_js.write(js.encode('utf-8') + ',\n')
            wf_py.write(js.encode('utf-8') + ',\n')
            i += 1
        else:
            wf_js.write(js.encode('utf-8') + '\n')
            wf_py.write(js.encode('utf-8') + '\n')

    wf_js.write("]};")
    wf_py.write("]}")
    wf_js.close()
    wf_py.close()


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

    archive_to_files(total)

if __name__ == '__main__':
    main()
