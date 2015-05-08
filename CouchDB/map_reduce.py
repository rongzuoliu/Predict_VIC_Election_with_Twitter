from couchdb.design import ViewDefinition

__author__ = 'rongzuoliu'
# coding=utf-8

import couchdb
import time
import re
import json


def map_reduce(dbname, search_term):
    s_time = time.time()
    server = couchdb.Server()
    db = server[dbname]

    w_file_path = "../RawTweets/raw_" + dbname + "_" + search_term + ".txt"
    wf = open(w_file_path, 'w')

    map_fun = '''
    function(doc) {
      if (doc.text.search(/''' + search_term + '''/) != -1) {
        emit(doc.id, {userID: doc.user.id, tweetID: doc.id, geoLocation: doc.geoLocation, place: doc.place, location: doc.user.location, text: doc.text, createdAt: doc.createdAt});
      }
    }'''


    print '\nstart to map reduce...........'
    print 'searching: %s in database: %s............\n' %(search_term, dbname)

    for row in db.query(map_fun):
        print row.value
        js = json.dumps(row.value, ensure_ascii=False)
        # print js
        wf.write(re.sub(r'\n', ' ', js.encode('utf-8')) + '\n')
    e_time = time.time()

    wf.close()
    print ("\nUse time: %s\n" % str(e_time-s_time))
    print ("\nResult stored in %s" % w_file_path)


def main():
    terms = ['DanielAndrewsMP', 'Daniel Andrews', 'Labor',
            'denisvnapthine', 'Denis Napthine', 'Liberal',
            'GregMLC', 'Greg Barber', "Greens"
    ]
    dbs = ['tweets2010', 'tweets2011', 'tweets2012', 'tweets2013']


def main():

    terms = [
        'DanielAndrewsMP', 'Daniel Andrews', 'Labor',
        'denisvnapthine', 'Denis Napthine', 'Liberal',
        'GregMLC', 'Greg Barber', "Greens"
    ]

    dbs = ['tweets2010', 'tweets2011', 'tweets2012', 'tweets2013']

    for term in terms:
        map_reduce("tweets2010", term)
    map_reduce("test", 'mel')


if __name__ == '__main__':
    main()
