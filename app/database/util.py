# database/util.py
# Written by Alessandra Laudando

from flask import url_for

def generate_post_data(query):
    '''
        Generate the post data
        :query: {}
        :return: {}
    '''
    post_data = {
        'author': query['author'],
        'author_id': query['author_id'],
        'body': query['body'],
        'documents': query['documents'],
        'id': str(query['_id']),
        'images': query['images'],
        'time': query['time'],
        'title': query['title'],
        'post_type': query['post_type'],
        }
    return post_data
