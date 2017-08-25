# database/util.py
# Written by Alessandra Laudando

from flask import url_for

def post_to_dict(query):
    '''
        Converts MongoDB post object to a python dictionary,
        for easy conversion to a json object.
        :query: {}
        :return: {}
    '''
    post = {
        'id': str(query['_id']),
        'author': query['author'],
        'body': query['body'],
        'documents': get_file_urls(query['documents']),
        'images': get_file_urls(query['images']),
        'time': query['time'],
        'title': query['title'],
        'type': query['type'],  
    }
    return post

def get_file_urls(image_paths):
    images = []
    for path in image_paths:
        images.append(url_for('uploads.get_file', filename=path, _external=True))
        
    return images
    