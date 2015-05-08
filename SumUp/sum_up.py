__author__ = 'rongzuoliu'

import re
import json
import time
import os


# todo: separate parites into a file
parties = ['Labor', 'Liberal', 'Greens']

def sum_prediction(r_path):

    count_pos = 0
    count_neu = 0
    count_neg = 0
    count_none = 0
    total = 0
    towards = ''

    with open(r_path) as file:
        for line in file:
            js = json.loads(line)
            sentiment = js['sentiment']
            if (sentiment == 'pos'):
                count_pos += 1
            elif (sentiment == 'neu'):
                count_neu += 1
            elif (sentiment == 'neg'):
                count_neg += 1
            else:
                count_none += 1
            total += 1
            towards = js['towards']

    return (towards, count_pos, count_neu, count_neg, count_none, total)


    #
    # to_Lable = re.findall('Labor'.lower(), term.lower(), 0) or re.findall('Daniel'.lower(), term.lower(), 0)
    # to_Liberal = re.findall('Liberal'.lower(), term.lower(), 0) or re.findall('Denis Napthine'.lower(), term.lower(), 0)
    # to_Greens = re.findall('')
    # if (to_Lable):



def main():

    r_paths = []
    direct_path = "../LabelledTweets"
    for file in os.listdir(direct_path):
        if file.endswith(".txt"):
            r_paths.append(direct_path + '/' + file)


    w_path = "test.txt"
    wf = open(w_path, 'w')
    s_time = time.time()


    # todo: check if electorate is null, what will happen

    # initialisation
    counts = {'pos': 0, 'neu': 0, 'neg': 0, 'none': 0}
    rates = {'posRate': 0.0, 'neuRate': 0.0, 'negRate': 0.0, 'noneRate': 0.0}
    party_counts = {}
    party_rates = {}
    for party in parties:
        party_counts[party] = dict(counts)
        party_rates[party] = dict(rates)
    result = {}
    result['name'] = ''
    result['parties'] = dict(party_rates)

    with open('../DataSource/electorateFeatures.json') as f:
        js_old = json.load(f)
        # each feature contains the whole information about an electorate
        for feature in js_old['features']:
            name = feature['properties'].get('Name')
            result['name'] = name
            result['parties'] = dict(party_rates)
            js_new = json.dumps(result, ensure_ascii=False)
            wf.write(js_new.encode('utf-8') + '\n')
    wf.close()

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



    total_pos = 0
    total_neu = 0
    total_neg = 0
    total_none = 0
    total = 0.0 # for division

    # todo: test
    # r_path = ['../LabelledTweets/labelled_tweets2010_Greens.txt']
    for r_path in r_paths:
        print '\nCounting in file %s' % r_path
        # sum up the predicted result of a given labelled file
        (towards, count_pos, count_neu, count_neg, count_none, sub_total) = sum_prediction(r_path)
        print 'Towards: %s' %towards
        print 'Count of Pos: %s' %count_pos
        print 'Count of Neu: %s' %count_neu
        print 'Count of Neg: %s' %count_neg
        print 'Count of None: %s' %count_none

        total += sub_total
        for party, counts in party_counts.iteritems():
            if party == towards_party(towards):
                counts['pos'] += count_pos
                counts['neg'] += count_neg
                counts['neu'] += count_neu
                counts['none'] += count_none
    print party_counts
    print total



    e_time = time.time()
    last_time = e_time - s_time
    print '\nUse time: %s \n' % last_time
    print '\nResult is stored in %s \n' % w_path



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
