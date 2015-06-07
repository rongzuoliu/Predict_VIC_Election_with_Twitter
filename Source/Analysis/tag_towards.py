__author__ = 'rongzuoliu'
# coding=utf-8

import re
import couchdb

#import source files
from POLITICLASS import PARTIES, LEADERS, PARTYANDLEADER


def tag_textTo(db, doc):
    to_party = []
    to_leader = []
    if ('text' in doc):
        for party in PARTIES:
            # print party
            find_party = re.findall(party, doc['text'], 0)
            if (find_party):
                for p in find_party:
                    if (not (p in to_party)):
                        to_party.append(p)
        for leader in LEADERS:
            find_leader = re.findall(leader, doc['text'], 0)
            if (find_leader):
                for l in find_leader:
                    if (not (l in to_leader)):
                        to_leader.append(l)
        doc['textTo'] = {'toParty': to_party, 'toLeader': to_leader}
        print doc['textTo']
        print '\n'
        db.save(doc)


def tag_towards(db, doc):
    towards = ''
    is_tag = True
    # Both hashtags and inReplyToScreenName could contain parties' or leaders' names
    # Both hashtags and inReplyToScreenName are already recorded into the 'textTo' field
    # But the difference is there must only one name in 'inReplyToScreenName' and this field means the tweet is used to reply this name
    hashtags = []
    for ht in doc['hashtagEntities']:
        hashtags.append(ht['text'])
    # Way 1:
    # Therefore, the name in 'inReplyToScreenName' is extremely useful to be used in tag party/leader.
    if 'inReplyToScreenName' in doc:
        inReplyToScreenName = doc['inReplyToScreenName']
        if inReplyToScreenName:
            # print 'inReplyToScreenName: %s' % inReplyToScreenName
            for party, party_and_leader in PARTYANDLEADER.iteritems():
                if re.findall(party.lower(), inReplyToScreenName.lower(), 0):
                    # print 'found %s' % inReplyToScreenName
                    towards = party
                    doc['towards'] = towards
                    db.save(doc)
                    print 'Tweet %s uses way 1: %s' % (doc.id, towards)
                    print doc['textTo']
                    return is_tag
    # Way 2:
    # Similarly, look for 'retweetedStatus' field.
    if 'retweetedStatus' in doc:
        retweetedStatus = doc['retweetedStatus']
        if retweetedStatus:
            retweetedTo = doc['retweetedStatus']['user']['screenName']
            for party, party_and_leader in PARTYANDLEADER.iteritems():
                if re.findall(party.lower(), retweetedTo.lower(), 0):
                    # print 'found %s' % inReplyToScreenName
                    towards = party
                    doc['towards'] = towards
                    db.save(doc)
                    print 'Tweet %s uses way 2: %s' % (doc.id, towards)
                    print doc['textTo']
                    return is_tag
    # Way 3, 4, 5:
    if 'textTo' in doc:
        if doc['textTo'] != None:
            to_leader = doc['textTo']['toLeader']
            to_party = doc['textTo']['toParty']
            if len(to_leader)==0 and len(to_party)==1:
                towards = to_party[0]
                print 'Tweet %s uses way 3: %s' % (doc.id, towards)
            elif len(to_leader)==1 and len(to_party)==0:
                # print to_leader
                for party, party_and_leader in PARTYANDLEADER.iteritems():
                    if to_leader[0] in party_and_leader:
                        towards = party
                print 'Tweet %s use way 4: %s' % (doc.id, towards)
            elif len(to_leader)==1 and len(to_party)==1:
                for party, party_and_leader in PARTYANDLEADER.iteritems():
                    if to_party[0]==party and to_leader[0] in party_and_leader:
                        towards = party
                print 'Tweet %s use way 5: %s' % (doc.id, towards)
            else:
                is_tag = False
            doc['towards'] = towards
            db.save(doc)
        else:
            print '\'textTo\' field is None.'
    else:
        print '\'textTo\' field is not exist.'
    return is_tag


def main():
    server = couchdb.Server('http://127.0.0.1:5984/')
    db = server['vic_election']

    tagged_count = 0
    for id in db:
        doc = db.get(id)
        if ('textTo' not in doc):
            tag_textTo(db, doc)
            if ('towards' not in doc):
                if tag_towards(db, doc):
                    tagged_count += 1
            else: print 'Tweets %s\'s towards already has been tagged.' % id
        else:
            print 'Tweet %s\'s textTo already has been tagged.' % id
    print 'Tagged: %s tweets.' % tagged_count


if __name__ == "__main__":

    main()









