__author__ = 'rongzuoliu'
# coding=utf-8

import couchdb

def create_map_function(term):
    map_fun = '''
    function(doc) {
      if (doc.text.search(/''' + term + '''/) != -1) {
        emit(doc.id, {userID: doc.user.id, tweetID: doc.id, geoLocation: doc.geoLocation, place: doc.place, location: doc.user.location, text: doc.text, createdAt: doc.createdAt});
      }
    }'''
    return map_fun


def main():
    server = couchdb.Server('http://127.0.0.1:5984/')
    db_names = ['liberal_followers']
    terms = ['Labor', 'Liberal', 'Greens']
    views = {}
    for db_name in db_names:
        db = server[db_name]
        design = {'views': views}
        for term in terms:
            view_name = term
            views[view_name] = {'map': create_map_function(term)}
            create_map_function(term)
            design['views'] = views
        db['_design/mapviews'] = design

### the structure of design dictionary:
    # design = {
    #     'views': {
    #         view_name: {
    #             'map': map_fun
    #         }
    #     }
    # }
###


if __name__ == '__main__':
    main()
