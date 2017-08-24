# database/__init__.py
# Written by Jeff Kaleshi

from pymongo import MongoClient

class Database():
    '''Manages post database CRUD operations'''

    def init_app(self, app):
        '''Configures Database'''
        db_uri = app.config['DB_URI']
        db_port = app.config['DB_PORT']
        db_name = app.config['DB_NAME']

        self._connection = MongoClient(db_uri, db_port)
        self._collection = self._connection[db_name]

    def add_post(self, post):
        '''
            Save post to database
            :posts: {}
            :return: {} 
        '''
        pass

    def get_n_posts(self, n):
        '''
            Get n posts from the database
            :n: int
            :return: [{}, {}, ...]
        '''
        pass

    def get_post(self, id):
        '''
            Get a single post from the database
            :id: int
            :return: {}
        '''
        pass

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