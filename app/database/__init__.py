# database/__init__.py
# Written by Jeff Kaleshi

from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId

from .util import post_to_dict

class Database():
    '''Manages post database CRUD operations'''

    def init_app(self, app):
        '''Configures Database'''
        db_uri = app.config['DB_URI']
        db_port = app.config['DB_PORT']
        db_name = app.config['DB_NAME']

        self._connection = MongoClient(db_uri, db_port)
        self._db = self._connection[db_name]
        self._collection = self._db['posts']

    def add_post(self, post):
        '''
            Save post to database
            :data: {}
            :return: {} 
        '''
        self._collection.insert_one(post)
        return post_to_dict(post)
        
    def get_n_posts(self, start_post, start_time, num_posts):
        '''
            Get n posts from the database
            :num_posts: int
            :return: [{}, {}, ...]
        '''
        query = self._collection.find({'time': {'$lte': start_time}})  \
                                .sort('time', DESCENDING) \
                                .skip(start_post) \
                                .limit(num_posts)

        posts = []
        for item in query:
            post = post_to_dict(item)
            posts.append(post)
        
        return posts
        

    def get_post(self, id):
        '''
            Get a single post from the database
            :id: int
            :return: {}
        '''
        query = self._collection.find_one({'_id': ObjectId(id) })
        post = post_to_dict(query)
        return post

    def edit_post(self, id):
        '''
            Edit a single a post from the database
            :id: int
            :return: {}
        '''
        pass

    def delete_post(self, id):
        '''
            Delete a single post from the database
            :id: int
            :return: {}
        '''
        pass