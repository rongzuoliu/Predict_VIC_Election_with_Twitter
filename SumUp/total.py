

__author__ = 'rongzuoliu'

import re
import json
import time
import os
import copy


def main():

    elect_counts = []

    # Get data from json file
    with open('../SumUp/electData.json') as f:
        js_old = json.load(f)
        for line in js_old['counts']:
            electorate = line['electorate']
            elect_counts.append(copy.deepcopy(electorate['parties']))
            # print electorate
            # print electorate['parties']
    # for term in party_counts:
    #     print term

    parties = ['Labor', 'Liberal', 'Greens', 'Nationals']
    one_party_sum = {'total_pos': 0, "total_neg": 0, "total_neu": 0, "total": 0, 'pos_rate': 0, 'neu_rate': 0, 'neg_rate': 0}
    parties_sum = {}
    for party in parties:
        parties_sum[party] = copy.deepcopy(one_party_sum)

    print parties_sum

    for elect in elect_counts:
        print elect
        for party in elect:
            sentiments = elect[party]
            print sentiments
            for senti in sentiments:
                print senti
                if senti == 'pos':
                    parties_sum[party]['total_pos'] += sentiments[senti]
                elif senti == 'neu':
                    parties_sum[party]['total_neu'] += sentiments[senti]
                elif senti == 'neg':
                    parties_sum[party]['total_neg'] += sentiments[senti]
                elif senti == 'total':
                    parties_sum[party]['total'] += sentiments[senti]

    print parties_sum


    wf = open('electDataSum.js', 'w')
    wf.write("var electDataSum = {\n\"type\": \"Sum of Predicted Election Results \",\n\"parties\": {\n")

    js = json.dumps(parties_sum, ensure_ascii=False)

    wf.write('%s\n}}' % js)
    wf.close()







if __name__ == '__main__':
    main()