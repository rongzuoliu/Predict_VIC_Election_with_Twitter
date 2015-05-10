import copy

__author__ = 'rongzuoliu'

import re
import json
import time
import os


# todo: separate parites into a file
# todo: check if electorate is null, what will happen


# initialisation
parties = ['Labor', 'Liberal', 'Greens']
counts = {'pos': 0, 'neu': 0, 'neg': 0, 'none': 0, 'total': 0}
party_counts = {}
for party in parties:
    party_counts[party] = copy.deepcopy(counts)
elect_counts = {}
elect_counts['name'] = ''
elect_counts['parties'] = copy.deepcopy(party_counts)

total_counts = []

with open('../DataSource/electorateFeatures.json') as f:
    js_old = json.load(f)
    # each feature contains the whole information about an electorate
    for feature in js_old['features']:
        name = feature['properties'].get('Name')
        elect_counts['name'] = name
        elect_counts['parties'] = copy.deepcopy(party_counts)
        total_counts.append({'electorate': copy.deepcopy(elect_counts)})

# total_counts.append({'electorate': {'name': 'None', 'parties': copy.deepcopy(party_counts)}})
# print total_counts



############################function definitions###########################################

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




def sum_prediction(r_path):
    print '\n\nProcessing with file: %s \n' % r_path
    file_total = 0
    towards = ''
    if (os.stat(r_path).st_size !=  0):
        with open(r_path) as file:
            for line in file:
                js = json.loads(line)
                sentiment = js['sentiment']
                electorate = js['electorate']
                towards = js['towards']

                for elect in total_counts:
                    if elect['electorate']['name'] == electorate: # This tweet is belong to this electorate
                        print elect
                        party = towards_party(towards) # This tweet is towards to this party
                        if (sentiment == 'pos'):
                            elect['electorate']['parties'][party]['pos'] += 1
                        elif (sentiment == 'neu'):
                            elect['electorate']['parties'][party]['neu'] += 1
                        elif (sentiment == 'neg'):
                            elect['electorate']['parties'][party]['neg'] += 1
                        else:
                            elect['electorate']['parties'][party]['none'] += 1

                        # sum up the total sentiment result for this party in this electorate
                        elect['electorate']['parties'][party]['total'] += 1
                        file_total += 1
                    else: # This tweet isn't belong to any of these electorates
                        pass # todo: when tweet isn't belong to any electorates

    return file_total



def main():

    total = 0.0 # for division

    r_paths = []
    direct_path = "../LabelledTweets"
    for file in os.listdir(direct_path):
        if file.endswith(".txt"):
            r_paths.append(direct_path + '/' + file)

    for r_path in r_paths:
        # sum up the predicted result of a given labelled file
        sub_total = sum_prediction(r_path)
        total += sub_total

    # # todo: test
    # r_path = '../LabelledTweets/Labelled_tweets2010_Daniel Andrews.txt'
    # sub_total = sum_prediction(r_path)
    # total += sub_total
    #
    # r_path = '../LabelledTweets/labelled_tweets2010_Denis Napthine.txt'
    # sub_total = sum_prediction(r_path)
    # total += sub_total


    print total
    print total_counts

    wf = open('test_count.txt', 'w')
    wf.write("var electData = {\n\"type\": \"Counts of Predicted Election Results \",\n\"counts\": [\n")

    i = 0
    for elect in total_counts:
        js = json.dumps(elect, ensure_ascii=False)
        if i < len(total_counts)-1:
            wf.write(js.encode('utf-8') + ',\n')
            i += 1
        else:
            wf.write(js.encode('utf-8') + '\n')

    wf.write("]};")
    wf.close()





if __name__ == '__main__':
    main()
