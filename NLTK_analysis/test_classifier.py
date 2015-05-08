__author__ = 'rongzuoliu'

import re, math, collections, itertools
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist


def evaluate_features(feature_select):
    #reading pre-labeled input and splitting into lines
    posSentences = open('rt-polarity.pos', 'r')
    negSentences = open('rt-polarity.neg', 'r')
    posSentences = re.split(r'\n', posSentences.read())
    negSentences = re.split(r'\n', negSentences.read())

    posFeatures = []
    negFeatures = []

    #http://stackoverflow.com/questions/367155/splitting-a-string-into-words-and-punctuation
    #breaks up the sentences into lists of individual words (as selected by the input mechanism) and appends 'pos' or 'neg' after each list
    for i in posSentences:
        posWords = re.findall(r"[\w']+|[.,!?;]", i)
        # posWords = [feature_select(posWords), 'pos']
        posWords = feature_select.append((posWords), 'pos')
        posFeatures.append(posWords)

    for i in negSentences:
        negWords = re.findall(r"[\w']+|[.,!?;]", i)
        # negWords = [feature_select(negWords), 'neg']
        # negWords =
        negFeatures.append(negWords)

    print posFeatures
    print negFeatures

    #selects 3/4 of the features to be used for training and 1/4 to be used for testing
    posCutoff = int(math.floor(len(posFeatures)*3/4))
    negCutoff = int(math.floor(len(negFeatures)*3/4))
    trainFeatures = posFeatures[:posCutoff] + negFeatures[:negCutoff]
    testFeatures = posFeatures[posCutoff:] + negFeatures[negCutoff:]

    classifier = NaiveBayesClassifier.train(trainFeatures)

    # referenceSets
    # for i, (features, label) in enumerate(testFeatures):
    #     referenceSets[label].add(i)
    #     predicted = classifier.classify(features)
    #     testSets[predicted].add(i)
    #
    # print 'train on %d instances, test on %d instances' % (len(trainFeatures), len(testFeatures))
    # print 'accuracy:', nltk.classify.util.accuracy(classifier, testFeatures)
    # print 'pos precision:', nltk.metrics.precision(referenceSets['pos'], testSets['pos'])
    # print 'pos recall:', nltk.metrics.recall(referenceSets['pos'], testSets['pos'])
    # print 'neg precision:', nltk.metrics.precision(referenceSets['neg'], testSets['neg'])
    # print 'neg recall:', nltk.metrics.recall(referenceSets['neg'], testSets['neg'])
    # classifier.show_most_informative_features(10)



if __name__ == '__main__':
    print 'using all words as features'
    make_full_dict = []
    evaluate_features(make_full_dict)
    #
    # result = self.classifier.classify(self.extract_features(a_tweet.split()))
    # print result
