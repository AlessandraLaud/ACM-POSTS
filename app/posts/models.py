# posts/models.py
# Written by Jeff Kaleshi

# POST SEARCH TYPES
AUTHOR = 'author'
BODY = 'body'
DOCUMENTS = 'documents'
ID = '_id'
IMAGES = 'images'
TIME = 'time'
TITLE = 'title'
POST_TYPE = 'post_type'

class Post():

    def __init__(
        self, author, author_id, body, documents, id, images, time, title, post_type):
        '''
        Structure to store or post data
        '''
        self.author = author
        self.author_id = author_id
        self.body = body
        self.documents = documents
        self.id = id
        self.images = images
        self.time = time
        self.title = title
        self.post_type = post_type

    def get_json(self):
        '''
        Get the dictionary in order to use jsonify
        :return: {}
        '''
        post = {
            'author': self.author,
            'author_id': self.author_id,
            'body': self.body,
            'documents': self.documents,
            'id': self.id,
            'images': self.images,
            'time': self.time,
            'title': self.title,
            'type': self.post_type,
        }

        return post
        
    def __str__(self):
        return "<Post: {}>".format(self.title)

    def __repr__(self):
        return "<Post: {}>".format(self.title)