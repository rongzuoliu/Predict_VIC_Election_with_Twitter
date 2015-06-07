__author__ = 'rongzuoliu'

import couchdb

def create_map_function(term):
    map_fun = '''
    function(doc) {
      if (doc.createdAt.search(/''' + term + '''/) != -1) {
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


def create_views(server, db_name, terms):
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


def main():
    server = couchdb.Server('http://127.0.0.1:5984/')
    db_name = 'test_towards'
    terms = ['2010', '2011', '2012', '2013', '2014']
    if db_name in server:
        create_views(server, db_name, terms)



if __name__ == '__main__':
    main()
