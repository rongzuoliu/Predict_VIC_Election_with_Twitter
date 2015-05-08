__author__ = 'rongzuoliu'

from TextParser import *
from SentiAnalyseWithTextBlob import *


# todo: parsing as the format of:
# todo: UserID;;;;;;;;TweetID;;;;;;;;Text;;;;;;;;CreatedAt;;;;;;;;Location;;;;;;;;Lat;;;;;;;;Lon;;;;;;;;Electorate

class TweetParser:
    UserID = 0
    TweetID = 0
    Text = ''
    CreatedAt = ''
    Location = ''
    Lat = 200.00 # invalid lat
    Lon = 200.00 # invalid lon
    Electorate = ''

    Sentiment = ''
    Place = ''
    GeoLocation = ''

    AtUser = []
    HashTag = []
    FeatureVector = []

    def __init__(self, line):
        self.self = self
        tokens = line.split(';;;;;;;;')

        self.UserID = tokens[0]
        self.TweetID = tokens[1]
        self.Text = tokens[2]
        self.CreatedAt = tokens[3]
        self.Location = tokens[4]
        self.Lat = tokens[5]
        self.Lon = tokens[6]
        self.Electorate = tokens[7]

        textParser = TextParser()
        self.FeatureVector = textParser.parsing(self.Text)
        # Important: AtUser and HashTag only exist after parsing text
        self.AtUser = textParser.AtUser
        self.HashTag = textParser.HashTag
        self.Sentiment = self.getTweetSenti()


    def getTweetSenti(self):
        string = ' '.join(self.FeatureVector)
        # return sentiAnalysisWithTextBlob(string, "NaiveBayesAnalyzer")
        return sentiAnalysisWithTextBlob(string, "PatternAnalyzer")

#
# def main():
#     file_path = "../CouchDB/copy of tweets2010_Greens.txt"
#     start_l = 2
#     end_l = 10
#     with open(file_path) as file:
#         sliced_file = islice(file, start_l, end_l)
#         for i, line in enumerate(sliced_file):
#             tweet = TweetParser(line)
#             print tweet.Text
#             # print tweet.FeatureVector
#             print tweet.Sentiment


if __name__ == '__main__':
    # main()
    print 'error!!!'
    print 'The \'(not_)TweetParser.py\' is a class, which shouldn\'t be called alone!'



