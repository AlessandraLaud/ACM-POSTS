# posts/input_parsers.py
# Written by Alessandra Laudando

from pymongo import DESCENDING, ASCENDING

from flask import request

def add_post_parser(request):
    request_data = {
        'images': request.files.getlist('images'),
        'documents': request.files.getlist('documents'),
        'body': request.form.get('body'),
        'title': request.form.get('title'),
        'post_type': request.form.get('type'),
    }
    return request_data

def update_post_parser(request):
    '''
    Parse through the updated post data
    :request: request object 
    :return: {}
    '''
    request_data = {}
    body = request.form.get('body')
    title = request.form.get('title')
    post_type = request.form.get('type')

    if body != None:
        request_data['body'] = body
    if title:
        request_data['title'] = title
    if post_type:
        request_data['type'] = post_type

    return request_data

def get_n_posts_parser(request):
    '''
    Parse through the posts data
    :request: request object 
    :return: {}
    '''
    request_data = {}
    num_posts = request.args.get('numPosts')
    start_time = request.args.get('startTime')
    start_post = request.args.get('startPost')
    direction = request.args.get('direction')
    sort_by = request.args.get('sortBy')

    if num_posts:
        try:
            request_data['num_posts'] = int(num_posts)
        except ValueError:
            pass

    if start_time:
        try:
            request_data['start_time'] = int(start_time)
        except ValueError:
            pass

    if start_post:
        try:
            request_data['start_post'] = int(start_post)
        except ValueError:
            pass

    if direction:
        if direction == 'DESCENDING':
            request_data['direction'] = DESCENDING

    if sort_by:
        if sort_by == 'author':
            request_data['field_type'] = 'author'
        elif sort_by == 'body':
            request_data['field_type'] = 'body'
        elif sort_by == 'id':
            request_data['field_type'] = '_id'
        elif sort_by == 'time':
            request_data['field_type'] = 'time'
        elif sort_by == 'title':
            request_data['field_type'] = 'title'
        elif sort_by == 'post_type':
            request_data['field_type'] = 'post_type'
    
    return request_data