__author__ = 'rongzuoliu'

from textblob.en.sentiments import NaiveBayesAnalyzer, PatternAnalyzer
from textblob import TextBlob

def sentiAnalysisWithTextBlob(string, classifier):

    sentiment = ''
    if (classifier == "NaiveBayesAnalyzer"):
        blob = TextBlob(string, analyzer= NaiveBayesAnalyzer())
        # print blob.tags
        # print blob.sentiment
        sentiment = blob.sentiment.classification

    elif (classifier == "PatternAnalyzer"):
        blob = TextBlob(string)
        # print blob.sentiment
        if (blob.sentiment.polarity > 0):
            sentiment = 'pos'
        elif (blob.sentiment.polarity == 0):
            sentiment = 'neu'
        elif (blob.sentiment.polarity < 0):
            sentiment = 'neg'

    return sentiment



if __name__ == '__main__':
    print 'error!!!'
    print 'The \'SentiAnalyseWithTextBlob.py\' is a function file, which shouldn\'t be called alone!'

