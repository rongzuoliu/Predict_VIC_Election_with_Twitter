__author__ = 'rongzuoliu'
# coding=utf-8

import couchdb
import couchdb.http


def create_map_function(term):
    map_fun = '''
    function(doc) {
      if (doc.text.search(/''' + term + '''/) != -1) {
        emit(doc.id, {userID: doc.user.id, tweetID: doc.id, geoLocation: doc.geoLocation, place: doc.place, location: doc.user.location, text: doc.text, createdAt: doc.createdAt});
      }
    }'''
    return map_fun


###
# the structure of design dictionary:
    # design = {
    #     'views': {
    #         view_name: {
    #             'map': map_fun
    #         }
    #     }
    # }
###


def create_views(server, db_names, terms):
    for db_name in db_names:
        db = server[db_name]

        if '_design/mapviews' in db:
            pass
        else:
            db['_design/mapviews'] = {'views': {}}

        doc = db.get('_design/mapviews')
        for term in terms:
            new_view = term
            if new_view not in doc['views']:
                doc['views'][new_view] = {'map': create_map_function(term)}
                print 'Created a new view: %s in the \'_design/mapviews\' file of the database %s.' % (new_view, db_name)
            else:
                print 'The view %s already exsits in the database %s.' % (new_view, db_name)
        db.save(doc)



def combine_views(server, db_names, new_db_name):
    ids = []
    new_db = server[new_db_name]
    for db_name in db_names:
        db = server[db_name]
        if '_design/mapviews' in db:
            views = db['_design/mapviews']['views'].keys()
            view_names = []
            for v in views:
                view_names.append('mapviews/'+v)
            for view in view_names:
                print 'Start to combine view %s from database %s into %s.' % (view, db_name, new_db_name)
                for row in db.view(view):
                    id = row.id
                    if id not in ids:
                        ids.append(id)
                        doc = db.get(id)
                        doc_new = doc
                        doc_new['_id'] = str(doc['id'])
                        try:
                            new_db.save(doc_new)
                        except (couchdb.ResourceConflict) as e:
                            print "Exception: Fail to archive tweet % s in database %s! Duplicated tweet!" % (str(doc_new['_id']), db_name)
        else:
            print 'There is no views to combine in the \'_design/mapviews\' file of database %s.' % db_name
            print 'Please create views in a file named \'_design/mapviews\' in database %s first.\n' % db_name



def main():
    server = couchdb.Server('http://127.0.0.1:5984/')
    db_names = ['tweets2010', 'tweets2011', 'tweets2012', 'tweets2013', 'tweets2014']
    terms = ['Labor', 'Daniel Andrews', 'DanielAndrewsMP',
             'Liberal', 'Napthine',
             'Greens', 'Greg Barber', 'GregMLC',
             'Nationals']

    # create_views(server, db_names, terms)

    # combine tweets in different views, delete replication, then store in a new db
    new_db_name = 'vic_election'
    # new_db_name = 'test_towards'
    if new_db_name in server:
        pass
    else:
        server.create(new_db_name)
    combine_views(server, db_names, new_db_name)

if __name__ == '__main__':
    main()
