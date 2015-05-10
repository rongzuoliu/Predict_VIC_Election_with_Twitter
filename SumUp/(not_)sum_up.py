import copy

__author__ = 'rongzuoliu'

import re
import json
import time
import os


# todo: separate parites into a file
# todo: check if electorate is null, what will happen

parties = ['Labor', 'Liberal', 'Greens']

w_path = "test.txt"
wf = open(w_path, 'w')
s_time = time.time()

# initialisation
counts = {'pos': 0, 'neu': 0, 'neg': 0, 'none': 0}
rates = {'posRate': 0.0, 'neuRate': 0.0, 'negRate': 0.0, 'noneRate': 0.0}
party_counts = {}
party_rates = {}
for party in parties:
    party_counts[party] = copy.deepcopy(counts)
    party_rates[party] = copy.deepcopy(rates)

print party_counts

elect_rates = {}
elect_counts = {}
elect_rates['name'] = ''
elect_counts['name'] = ''
elect_rates['parties'] = copy.deepcopy(party_rates)
# elect_counts['parties'] = dict(party_counts)
elect_counts['parties'] = copy.deepcopy(party_counts)
print elect_counts
total_counts = []


with open('../DataSource/electorateFeatures.json') as f:
    js_old = json.load(f)
    # each feature contains the whole information about an electorate
    for feature in js_old['features']:
        name = feature['properties'].get('Name')
        elect_rates['name'] = name
        elect_counts['name'] = name
        elect_rates['parties'] = copy.deepcopy(party_rates)
        elect_counts['parties'] = copy.deepcopy(party_counts)
        total_counts.append({'electorate': copy.deepcopy(elect_counts)})
        # print total_counts[len(total_counts)-1]
        js_new = json.dumps(elect_rates, ensure_ascii=False)
        wf.write(js_new.encode('utf-8') + '\n')
    elect_rates['name'] = 'None'
    elect_rates['parties'] = copy.deepcopy(party_rates)
    js_new = json.dumps(elect_rates, ensure_ascii=False)
    wf.write(js_new.encode('utf-8') + '\n')
wf.close()

total_counts.append({'electorate': {'name': 'None', 'parties': copy.deepcopy(party_counts)}})


# wf2 = open('test2', 'w')
# with open('test.txt') as f:
#     for elect in f:
#         js_old = json.loads(elect)
#
#         js_old['parties']['Liberal']['noneRate'] = 999
#
#         js_new = json.dumps(js_old, ensure_ascii=False)
#         wf2.write(js_new.encode('utf-8') + '\n')
# wf2.close()



def sum_prediction(r_path):

    sub_total = 0
    towards = ''

    # print r_path

    if (os.stat(r_path).st_size !=  0):
        print 'Summing file: %s' % r_path
        with open(r_path) as file:
            for line in file:
                js = json.loads(line)
                sentiment = js['sentiment']
                electorate = js['electorate']
                towards = js['towards']
                party = towards_party(towards) # This tweet is towards to this party
                # print party

                for elect in total_counts:
                    if elect['electorate']['name'] == electorate: # This tweet is belong to this electorate
                        # print electorate
                        # for party in parties:
                        #     if party == towards_party(towards): # This tweet is towards to this party
                        print party
                        if (sentiment == 'pos'):
                            elect['electorate']['parties'][party]['pos'] += 1
                        elif (sentiment == 'neu'):
                            elect['electorate']['parties'][party]['neu'] += 1
                        elif (sentiment == 'neg'):
                            elect['electorate']['parties'][party]['neg'] += 1
                        else:
                            elect['electorate']['parties'][party]['none'] += 1
                        sub_total += 1
                    else: # This tweet isn't belong to any electorates
                        pass # todo: when tweet isn't belong to any electorates
    print total_counts
    return sub_total



def main():

    total = 0.0 # for division

    r_paths = []
    direct_path = "../LabelledTweets"
    for file in os.listdir(direct_path):
        if file.endswith(".txt"):
            r_paths.append(direct_path + '/' + file)

    # todo: test
    # r_path = '../LabelledTweets/Labelled_tweets2010_Daniel Andrews.txt'

    for r_path in r_paths:
        # sum up the predicted result of a given labelled file
        sub_total = sum_prediction(r_path)
        total += sub_total

    print total

    e_time = time.time()
    last_time = e_time - s_time
    # print '\nUse time: %s \n' % last_time
    # print '\nResult is stored in %s \n' % w_path


    wf2 = open('sum_count.txt', 'w')
    for elect in total_counts:
        js = json.dumps(elect, ensure_ascii=False)
        wf2.write(js.encode('utf-8') + '\n')
    wf2.close()




def towards_party(towards):
    search_terms = [
        {"Labor": ['DanielAndrewsMP', 'Daniel Andrews', 'Labor']},
        {"Liberal": ['denisvnapthine', 'Denis Napthine', 'Liberal']},
        {"Greens": ['GregMLC', 'Greg Barber', "Greens"]},
        {"None": []}
    ]
    to_party = ''
    for line in search_terms:
        for party, terms in line.iteritems():
            if (towards in terms):
                to_party = party
    return to_party



if __name__ == '__main__':
    main()
