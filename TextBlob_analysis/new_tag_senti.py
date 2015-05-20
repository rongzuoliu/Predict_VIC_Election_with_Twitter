__author__ = 'rongzuoliu'

import couchdb

#import source files
from TextParser import *
from SentiAnalyseWithTextBlob import *


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

    print sentiment
    print senti_score

    return (sentiment, senti_score)



def tag_sentiment(db, view):
    # textParser = TextParser()
    for row in db.view(view):
        id = row.id
        doc = db.get(id)
        text = doc['text']
        (sentiment, senti_score) = sentiAnalysisWithTextBlob(text, "PatternAnalyzer")
        doc['sentiment'] = {"sentiment": sentiment, "sentiScore": senti_score}
        db.save(doc)



def main():
    server = couchdb.Server('http://127.0.0.1:5984/')
    db_names = ['liberal_followers']
    # view_names = ['mapviews/Labor', 'mapviews/Greens', 'mapviews/Liberal']
    view_names = ['mapviews/Labor']
    for db_name in db_names:
        db = server[db_name]
        for view in view_names:
            tag_sentiment(db, view)


if __name__ == '__main__':
    main()