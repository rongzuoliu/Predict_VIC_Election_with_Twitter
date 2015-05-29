__author__ = 'rongzuoliu'

import couchdb
from textblob.en.sentiments import NaiveBayesAnalyzer, PatternAnalyzer
from textblob import TextBlob

#import source files
# from TextParser import *


def sentiAnalysisWithTextBlob(string, classifier):
    sentiment = ''
    senti_score = -100
    if (classifier == "NaiveBayesAnalyzer"):
        blob = TextBlob(string, analyzer= NaiveBayesAnalyzer())
        # pos/neg is rang from 0-1, the number is bigger, the feeling is stronger
        senti_score = blob.sentiment.p_pos
        if (senti_score == 0.5):
            sentiment = 'neu'
        else:
            sentiment = blob.sentiment.classification

    elif (classifier == "PatternAnalyzer"):
        blob = TextBlob(string)
        senti_score = blob.sentiment.polarity
        if (blob.sentiment.polarity > 0):
            sentiment = 'pos'
        elif (blob.sentiment.polarity == 0):
            sentiment = 'neu'
        elif (blob.sentiment.polarity < 0):
            sentiment = 'neg'
    # print sentiment
    # print senti_score
    return (sentiment, senti_score)


def main():
    server = couchdb.Server('http://127.0.0.1:5984/')
    # db = server['vic_election']
    db = server['test_towards']
    for id in db:
        doc = db.get(id)
        text = doc['text']
        if ('towards' in doc):
            (sentiment, senti_score) = sentiAnalysisWithTextBlob(text, "PatternAnalyzer")
            doc['attitude'] = {"sentiment": sentiment, "sentiScore": senti_score}
            print str(sentiment) + ': '+str(senti_score)+'\n'
            db.save(doc)
        else:
            print 'tweets %s doesn\'t have a \'towards\' field.' % str(id)



if __name__ == '__main__':
    main()