

__author__ = 'rongzuoliu'

import re
import json
import time
import os
import copy


def main():

#{"electorate": {"name": "Albert Park", "parties": {"Liberal": {"neg": 3, "none": 0, "total": 18, "neu": 6, "pos": 9}, "Greens": {"neg": 5, "none": 0, "total": 41, "neu": 19, "pos": 17}, "Labor": {"neg": 18, "none": 0, "total": 85, "neu": 31, "pos": 36}}}},

    party_counts = []

    # Get data from json file
    with open('../SumUp/electData.json') as f:
        js_old = json.load(f)
        for line in js_old['counts']:
            electorate = line['electorate']
            # name = electorate['name']
            party_counts.append(copy.deepcopy(electorate['parties']))


    total_liberal = {'total_pos': 0, "total_neg": 0, "total_neu": 0, "total": 0, 'pos_rate': 0, 'neu_rate': 0, 'neg_rate': 0}
    total_labor = {'total_pos': 0, "total_neg": 0, "total_neu": 0, "total": 0, 'pos_rate': 0, 'neu_rate': 0, 'neg_rate': 0}
    total_greens = {'total_pos': 0, "total_neg": 0, "total_neu": 0, "total": 0.0, 'pos_rate': 0, 'neu_rate': 0, 'neg_rate': 0}

    for line in party_counts:
        # print line
        total_liberal['total'] += line['Liberal']['total']
        total_liberal['total_pos'] += line['Liberal']['pos']
        total_liberal['total_neu'] += line['Liberal']['neu']
        total_liberal['total_neg'] += line['Liberal']['neg']
        total_labor['total'] += line['Labor']['total']
        total_labor['total_pos'] += line['Labor']['pos']
        total_labor['total_neu'] += line['Labor']['neu']
        total_labor['total_neg'] += line['Labor']['neg']
        total_greens['total'] += line['Greens']['total']
        total_greens['total_pos'] += line['Greens']['pos']
        total_greens['total_neu'] += line['Greens']['neu']
        total_greens['total_neg'] += line['Greens']['neg']

    total_labor['pos_rate'] = total_labor['total_pos'] / float(total_labor['total'])
    total_labor['neu_rate'] = total_labor['total_neu'] / float(total_labor['total'])
    total_labor['neg_rate'] = total_labor['total_neg'] / float(total_labor['total'])

    total_liberal['pos_rate'] = total_liberal['total_pos'] / float(total_liberal['total'])
    total_liberal['neu_rate'] = total_liberal['total_neu'] / float(total_liberal['total'])
    total_liberal['neg_rate'] = total_liberal['total_neg'] / float(total_liberal['total'])

    total_greens['pos_rate'] = total_greens['total_pos'] / float(total_greens['total'])
    total_greens['neu_rate'] = total_greens['total_neu'] / float(total_greens['total'])
    total_greens['neg_rate'] = total_greens['total_neg'] / float(total_greens['total'])



    print total_liberal
    print total_labor
    print total_greens


    wf = open('electDataSum.js', 'w')
    wf.write("var electDataSum = {\n\"type\": \"Sum of Predicted Election Results \",\n\"parties\": {\n")

    js = json.dumps({"Labor": total_labor}, ensure_ascii=False)
    wf.write(js.encode('utf-8') + ',\n')
    js = json.dumps({"Liberal": total_liberal}, ensure_ascii=False)
    wf.write(js.encode('utf-8') + ',\n')
    js = json.dumps({"Greens": total_greens}, ensure_ascii=False)
    wf.write(js.encode('utf-8') + '\n')
    wf.write("}};")
    wf.close()







if __name__ == '__main__':
    main()