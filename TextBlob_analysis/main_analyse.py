__author__ = 'rongzuoliu'

import json
import time
import os

from TextParser import *
from SentiAnalyseWithTextBlob import *



def main():
    # file_path = "../ProprocessedTweets/geoed_tweets2010_Greens.txt"

    r_pathes = []
    direct_path = "../ProprocessedTweets"
    for file in os.listdir(direct_path):
        if file.endswith(".txt"):
            r_pathes.append(direct_path + '/' + file)

    for r_path in r_pathes:

        w_path = re.sub('../ProprocessedTweets/geoed_', '../LabelledTweets/labelled_', r_path)
        wf = open(w_path, 'w')

        s_time = time.time()

        textParser = TextParser()
        text = ''
        sentiment = ''
        print '\nstart to analyse the sentiment of the tweets...........'

        with open(r_path) as file:
            for line in file:
                js_old = json.loads(line)
                text = js_old['text']
                # sentiment = sentiAnalysisWithTextBlob(text, "NaiveBayesAnalyzer")
                sentiment = sentiAnalysisWithTextBlob(text, "PatternAnalyzer")
                js_old['sentiment'] = sentiment
                print sentiment

                js_new = json.dumps(js_old, ensure_ascii=False)
                wf.write(js_new.encode('utf-8') + '\n')
        wf.close()

        e_time = time.time()
        last_time = e_time - s_time
        print '\nUse time: %s \n' % last_time
        print '\nResult is stored in %s \n' % w_path


if __name__ == '__main__':
    main()