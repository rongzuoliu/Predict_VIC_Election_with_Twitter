__author__ = 'rongzuoliu'

import re

class TextParser:
    stopWordsFile = 'stop_words.txt'
    stopWords = []
    AtUser = []
    HashTag = []

    @staticmethod
    # get stop word list
    def getStopWords():
        #read the stopwords file and build a list
        TextParser.stopWords = []
        TextParser.stopWords.append('AT_USER')
        TextParser.stopWords.append('HASH_TAG')
        TextParser.stopWords.append('URL')
        fp = open(TextParser.stopWordsFile, 'r')
        line = fp.readline()
        while line:
            word = line.strip()
            TextParser.stopWords.append(word)
            line = fp.readline()
        fp.close()

    def parsing(self, text):
        text = self.replaceTags(text)
        feature_vector = self.getFeatureVector(text)
        parsed_text = ' '.join(feature_vector)
        return parsed_text


    # replace tags such as mentioned tweeters(@), hashtags(#), URL
    def replaceTags(self, text):
        #Convert to lower case
        text = text.lower()
        #Convert www.* or http?://* to URL
        text = re.sub('((www\.[^\s]+)|(http?://[^\s]+))', 'URL', text)
        #Convert @username to AT_USER
        self.AtUser = re.findall('@[^\s]+', text)
        text = re.sub('@[^\s]+','AT_USER', text)
        #Replace hashtag #word with the word
        # tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        self.HashTag = re.findall(r'#[^\s]+', text)
        text =  re.sub(r'#([^\s]+)', 'HASH_TAG', text)
        #Remove additional white spaces
        text = re.sub('[\s]+', ' ', text)
        #trim
        text = text.strip('\'"')
        return text


    # parse tweet to a feature vector
    def getFeatureVector(self, text):
        feature_vector = []
        #split tweet into words
        words = text.split()

        for w in words:
            #strip punctuation
            w = w.strip('\'"?,.')
            #check if the word stats with an alphabet
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
            #ignore if it is a stop word
            if(w in TextParser.stopWords or val is None):
                continue
            else:
                feature_vector.append(w.lower())
        return feature_vector



if __name__ == '__main__':
    # main()
    print 'error!!!'
    print 'The \'TextParser.py\' is a class, which shouldn\'t be called alone!'




