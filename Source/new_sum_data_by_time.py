__author__ = 'rongzuoliu'

import copy
import json
import re
import couchdb

from POLITICLASS import PARTIES


counts_by_dt = {}
counts = {'pos': 0, 'neu': 0, 'neg': 0, 'total': 0}
years = ['2010', '2011', '2012', '2013', '2014']
party_counts = {}
for party in PARTIES:
    party_counts[party] = copy.deepcopy(counts)
for year in years:
    counts_by_dt[year] = copy.deepcopy(party_counts)

print counts_by_dt
# for year, party_count in counts_by_dt.iteritems():
#     print year
#     print party_count


def try_to_count_in(doc):
    if_count = False
    created_year = ''
    # todo: change 'sentiment' to 'attitude'
    if 'attitude' in doc and 'electorate' in doc and 'towards' in doc:
        createdAt = doc['createdAt']
        year_list = re.findall('(2010|2011|2012|2013|2014)', createdAt, 0)
        if year_list:
            created_year = year_list[0]

        sentiment = doc['attitude']['sentiment']
        electorate = doc['electorate']
        towards = doc['towards']

        # The difference result compared with sum_data_counts is because this also count in the null electorate tweets
        if sentiment and towards and electorate:
            for year, count in counts_by_dt.iteritems():
                if year == created_year:
                    # print created_year
                    party = towards # This tweet is towards to this party
                    count[party][sentiment] += 1
                    print doc['id']
                    count[party]['total'] += 1
                    if_count = True
        else:
            print "sentiment, towards or electorate is None."
    else:
        print "sentiment, towards or electorate field is not exist."
    return if_count


def archive_to_files(total):
    wf_js = open('ELECTDATASUMBYTIME.js', 'w')
    wf_js.write('var electDataSumByTime = {\n\'type\': \'Counts of Predicted Election Results \',\n\'totalCount\': \'' + str(total) +'\',\n\'timeLines\': {\n')

    i = 0
    for year, party in counts_by_dt.iteritems():
        # js = json.dumps({year: party}, ensure_ascii=False)
        if i < len(counts_by_dt)-1:
            # wf_js.write(js.encode('utf-8') + ',\n')
            wf_js.write('\'%s\': %s,\n' % (year, party)) # valid format of javascript
            i += 1
        else:
            # wf_js.write(js.encode('utf-8') + '\n}};')
            wf_js.write('\'%s\': %s\n}};' % (year, party)) # valid format of javascript
    wf_js.close()


def main():
    total = 0
    server = couchdb.Server('http://127.0.0.1:5984/')
    db = server['vic_election']
    # db = server['test_towards']

    for id in db:
        doc = db.get(id)
        if try_to_count_in(doc):
            total += 1

    print counts_by_dt
    print total

    archive_to_files(total)


if __name__ == '__main__':
    main()
