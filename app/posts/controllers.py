# posts/controllers.py
# Written by Jeff Kaleshi

import os
from time import time

from flask import Blueprint, jsonify, request

from app import db
from .input_parsers import get_n_posts_parser, add_post_parser, \
                           update_post_parser
from .validate import validate_new_post, validate_update_post
from .util import save_files, create_posts_dictionary, \
                  get_post_with_urls, save_post
from .models import ID, Post


posts = Blueprint('posts', __name__)

@posts.route('/new', methods=['POST'])
def add_post():
    '''
    Add a new post
    :return: Json object
    '''   
    response = {'errors': [], 'post': {}}

    # parse request
    post_data = add_post_parser(request)

    # validate post data
    errors = validate_new_post(post_data)

    # set author and author_id
    post_data['author']= 'test'
    post_data['author_id'] = '00000'

    if errors:
        response['errors'] = errors
    else:
        try:
            post = save_post(post_data)
            post = get_post_with_urls(post)
            response['post'] = post.get_json()
        except Exception:
            response['errors'].append('Could not save post to database!')
        
    return jsonify(response)

@posts.route('/id/<id>', methods=['GET'])
def get_post(id):
    '''
    Get the post that corresponds to the id passed in 
    :id: String
    :return: Json object
    '''
    response = {'errors': [], 'post': None}

    try:
        posts = db.search_posts(id, ID)
        if posts:
            response['post'] = get_post_with_urls(posts[0]).get_json()
        else:
            response['errors'].append('Invalid Id!')
    except Exception:
        response['errors'].append('Could not get post from database!')

    return jsonify(response)

@posts.route('/', methods=['GET'])
def get_n_posts():
    '''
    Get the specified number of posts that corresponds to the id passed in 
    :return: Json object
    '''
    response = {'errors': [], 'posts': []}
    
    try:
        posts = db.search_posts(**get_n_posts_parser(request))
        response['posts'] = create_posts_dictionary(posts)
    except Exception:
        response['errors'] = 'Could get posts from database!'
    
    return jsonify(response)

@posts.route('/id/<id>', methods=['PUT'])
def update_post(id):
    '''
    Update an edited post
    :id: String
    :return: Json object
    '''
    response = {'errors': [], 'post': None}
    updated_fields = update_post_parser(request)
    error = validate_update_post(updated_fields)
    
    if error:
        response['errors'].append(error)
    else:
        post = db.update_post(id, updated_fields)
        if post:
            response['post'] = post.get_json()
        else:
            response['errors'].append('Invalid Id!')
        

    return jsonify(response)


@posts.route('/id/<id>', methods=['DELETE'])
def delete_post(id):
    '''
    Delete a post
    :id: String
    :return:
    '''
    response = {'errors': [], 'post': None}
    try:
        post = db.delete_post(id)
        if post:
            response['post'] = post.get_json()
        else:
            response['errors'].append('Invalid Id!')
    except Exception:
        response['errors'].append('Could not delete post from database!')
    return jsonify(response) 
