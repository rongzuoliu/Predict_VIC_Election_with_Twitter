__author__ = 'rongzuoliu'

from Classifier import *
from TweetParser_old import *
import re


if __name__ == '__main__':

    s_time = time.time()
    pos_tweets_file = '../train_and_test_tweets/rt-polarity.pos'
    neg_tweets_file = '../train_and_test_tweets/rt-polarity.neg'
    test_tweets_file = 'train_and_test_tweets/tweets2014_first_half.txt'
    wf = open('test_result.txt', 'w')

    # train classifier
    classifier = Classifier(pos_tweets_file, neg_tweets_file)

    # test classifier
    result_pos = 0
    result_neg = 0
    TweetParser.get_stop_words()
    parser = TweetParser()
    with open(test_tweets_file) as test:
        test_tweets = islice(test, 0, 200)
        for num, tweet in enumerate(test_tweets):
            print re.sub(r'\n', '', tweet)
            wf.write('%s \n' % re.sub(r'\n', '', tweet))
            parsed_tweet = parser.parser_tweets(tweet)
            print '%s \n' % parsed_tweet
            wf.write('%s \n' % parsed_tweet)
            result = classifier.predict_tweet(parsed_tweet)
            if (result == 'positive'):
                result_pos += 1
                wf.write("%s \n" % result)
            elif (result == 'negative'):
                result_neg += 1
                wf.write("%s \n" % result)
            wf.write('\n')
    wf.write('\n \n \n \n \n')
    wf.write("num of positive: %s \n" %result_pos)
    wf.write("num of negative: %s \n" %result_neg)
    print("num of positive: %s" %result_pos)
    print("num of negative: %s" %result_neg)
    e_time = time.time()
    wf.write("execution time: %s \n" %(e_time-s_time))
    print("execution time: %s" %(e_time-s_time))
    wf.close()


    # (4000/1000 test pos): 73.3% positive
    # (4500/500 test neg): 75.8% negative



    # fp = open('train_and_test_tweets/test_tweets.txt', 'r')
    # for line in fp:
    #     classifier.predict_tweet(line)

    # tweet = 'I love you'
    # classifier.predict_tweet(tweet)

