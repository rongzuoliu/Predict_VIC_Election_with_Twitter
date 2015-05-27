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
        doc = db.get('_design/mapviews')
        for term in terms:
            new_view = term
            if new_view not in doc['views']:
                doc['views'][new_view] = {'map': create_map_function(term)}
                print 'Created a new view: %s.' % new_view
            else:
                print 'The view %s already exsit.' % new_view
        db.save(doc)



def combine_views(server, db_names, new_db_name):
    ids = []
    new_db = server[new_db_name]
    for db_name in db_names:
        db = server[db_name]
        views = db['_design/mapviews']['views'].keys()
        view_names = []
        for v in views:
            view_names.append('mapviews/'+v)
        print view_names

        for view in view_names:
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
                        print "Exception: Fail to archive! Duplicated tweets!"



def main():
    server = couchdb.Server('http://127.0.0.1:5984/')
    db_names = ['liberal_followers']
    terms = ['Labor', 'Liberal', 'Greens', 'Nationals', 'Daniel Andrews', 'Napthine']

    create_views(server, db_names, terms)

    # combine tweets in different views, delete replication, then store in a new db
    new_db_name = 'vic_election'
    if new_db_name in server:
        pass
    else:
        server.create(new_db_name)
    combine_views(server, db_names, new_db_name)


if __name__ == '__main__':
    main()
