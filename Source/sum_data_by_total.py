__author__ = 'rongzuoliu'

import copy

#import source files
from ELECTDATACOUNTS import ELECTDATACOUNTS # need to execute sum_data_by_electorates.py first
from POLITICLASS import PARTIES

def main():
    one_party_sum = {'total_pos': 0, "total_neg": 0, "total_neu": 0, "total": 0, 'pos_rate': 0, 'neu_rate': 0, 'neg_rate': 0}
    parties_rates = {}
    for party in PARTIES:
        parties_rates[party] = copy.deepcopy(one_party_sum)
    print parties_rates

    for line in ELECTDATACOUNTS['counts']:
        for elect, counts in line.iteritems():
            party_counts = counts
        for party, p_count in party_counts.iteritems():
            print party
            print p_count
            senti_counts = p_count
            for senti in senti_counts:
                if senti == 'pos':
                    parties_rates[party]['total_pos'] += senti_counts[senti]
                elif senti == 'neu':
                    parties_rates[party]['total_neu'] += senti_counts[senti]
                elif senti == 'neg':
                    parties_rates[party]['total_neg'] += senti_counts[senti]
                elif senti == 'total':
                    parties_rates[party]['total'] += senti_counts[senti]

    total = 0
    for party in PARTIES:
        total += parties_rates[party]['total']
    print total
    for party in PARTIES:
        parties_rates[party]['pos_rate'] = parties_rates[party]['total_pos'] / float(total)
        parties_rates[party]['neu_rate'] = parties_rates[party]['total_neu'] / float(total)
        parties_rates[party]['neg_rate'] = parties_rates[party]['total_neg'] / float(total)

    wf_js = open('Results/TOTALDATARATES.js', 'w')
    wf_js.write('var totalDataRates = {\n\'type\': \'Sum of the Total Counts and Rates for Every Party\',\n\'total count\': ' + str(total) + ',\n\'parties\': {\n')
    i = 0
    for party in parties_rates:
        i += 1
        # js = json.dumps({party: parties_rates[party]}, ensure_ascii=False)
        if (i<len(parties_rates)):
            wf_js.write('\'%s\': %s,\n' % (party, parties_rates[party])) # valid format of javascript
            # wf_js.write(js.encode('utf-8') + ',\n')
        else:
            wf_js.write('\'%s\': %s\n}};' % (party, parties_rates[party])) # valid format of javascript
            # wf_js.write(js.encode('utf-8') + '\n}};')
    wf_js.close()



if __name__ == '__main__':
    main()