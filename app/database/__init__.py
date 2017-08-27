# database/__init__.py
# Written by Jeff Kaleshi

from pymongo import MongoClient, DESCENDING, ASCENDING
from bson.objectid import ObjectId
from bson.errors import InvalidId

from .util import generate_post_data
from app.posts.models import Post, ID, TIME

class Database():
    '''Manages post database CRUD operations'''

    def init_app(self, app):
        '''Configures Database'''
        db_uri = app.config['DB_URI']
        db_port = app.config['DB_PORT']
        db_name = app.config['DB_NAME']

        self._connection = MongoClient(db_uri, db_port, serverSelectionTimeoutMS=10)
        self._db = self._connection[db_name]
        self._collection = self._db['posts']

    def add_post(self, post):
        '''
            Save post to database
            :data: Post
            :return: Post
        '''
        self._collection.insert_one(post)
        post_data = generate_post_data(post)
        new_post = Post(**post_data)

        return new_post

    def search_posts(
        self, field=None, field_type=ID, start_time=None,
        start_post=0, num_posts=0, direction=ASCENDING):
        '''
            Searches database for posts that meet parameters
            :id: int
            :return: [Post, Post, ...]
        '''

        search = {}
        if field:
            if field_type is ID:
                try:
                    search[field_type] = ObjectId(field)
                except InvalidId:
                    return None
            else:
                search[field_type] = field

        if start_time != None:
            search[TIME] = {'$lte': start_time}

        query = self._collection.find(search) \
                .sort(field_type, direction) \
                .skip(start_post) \
                .limit(num_posts)

        posts = []
        for item in query:
            post_data = generate_post_data(item)
            posts.append(Post(**post_data))

        return posts

    def update_post(self, id, post):
        '''
            Edit a single a post from the database
            :id: int
            :form: MultiDict
            :return: {}
        '''
        try:
            filter = {'_id': ObjectId(id)}
        except InvalidId:
            return None

        if post != {}:
            self._collection.update_one(
                filter,
                {
                    '$set': post
                }
            )

        post = self.search_posts(id)
        if post:
            post = post[0]

        return post

    def delete_post(self, id):
        '''
            Delete a single post from the database
            :id: int
            :return: {}
        '''
        post = self.search_posts(id)

        if post:
            self._collection.delete_one({'_id': ObjectId(id)})
            post = post[0]
        else:
            post = None

        return post