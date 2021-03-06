__author__ = 'rongzuoliu'

import copy
import json
import couchdb

#import source files
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
    if 'attitude' in doc and 'electorate' in doc and 'towards' in doc:
        sentiment = doc['attitude']['sentiment']
        electorate = doc['electorate']
        towards = doc['towards']
        if sentiment and towards and electorate:
            for elect, count in elect_counts.iteritems():
                if elect == electorate: # This tweet is belong to this electorate
                    party = towards # This tweet is towards to this party
                    count[party][sentiment] += 1
                    count[party]['total'] += 1
                    if_count = True
                    print doc.id
                else: # This tweet isn't belong to any of these electorates
                    pass
    return if_count


def save_to_ELECTDATACOUNTS(total):
    wf_js = open('Predicted_Results/ELECTDATACOUNTS.js', 'w')
    wf_py = open('ELECTDATACOUNTS.py', 'w')
    wf_js.write('var electDataCounts = {\n\'type\': \'Sum Based on Electorates \',\n\'totalCount\': \'' + str(total) +'\',\n\'counts\': {\n')
    wf_py.write('ELECTDATACOUNTS = {\n\"type\": \"Sum Based on Electorates \",\n\"totalCount\": \"' + str(total) +'\",\n\"counts\": [\n')
    i = 0
    for elect, count in elect_counts.iteritems():
        js = json.dumps({elect: count}, ensure_ascii=False)
        if i < len(elect_counts)-1:
            wf_js.write('\'%s\': %s,\n' % (elect, count)) # valid format of javascript
            wf_py.write(js.encode('utf-8') + ',\n')
            i += 1
        else:
            wf_js.write('\'%s\': %s\n}};' % (elect, count)) # valid format of javascript
            wf_py.write(js.encode('utf-8') + '\n]}')
    wf_js.close()
    wf_py.close()


def main():
    total = 0
    server = couchdb.Server('http://127.0.0.1:5984/')
    db = server['vic_election']
    for id in db:
        doc = db.get(id)
        if try_to_count_in(doc):
            total += 1
    print total
    print elect_counts

    save_to_ELECTDATACOUNTS(total)

if __name__ == '__main__':
    main()
