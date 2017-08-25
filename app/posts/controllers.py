# posts/controllers.py
# Written by Jeff Kaleshi

import os
from time import time

from flask import Blueprint, jsonify, request

from app import db 
from .util import (get_post_from_form, save_files, IMAGE_EXTENSIONS,
                   DOCUMENT_EXTENSIONS, validate_files, validate_form)

posts = Blueprint('posts', __name__)

@posts.route('/new', methods=['POST'])
def add_post():   
    
    images = request.files.getlist('images')
    documents = request.files.getlist('documents')
    response = {'errors': [], 'post': {}}

    # validate images and documents
    form_valid = validate_form(request.form)
    images_valid = validate_files(images, 'images', IMAGE_EXTENSIONS)
    documents_valid = validate_files(documents, 'documents', DOCUMENT_EXTENSIONS)

    if form_valid != '':
        response['errors'].append(form_valid)
    if images_valid != '':
        response['errors'].append(images_valid)
    if documents_valid != '':
        response['errors'].append(documents_valid)
    
    if len(response) == 0: 
        post = get_post_from_form(request.form)
        images_path = save_files(images, 'images', 'jkales2')
        documents_path = save_files(documents, 'documents', 'jkales2')
        post['images'] = images_path
        post['documents'] = documents_path
        post['time'] = int(time())
        response['post'] = db.add_post(post)

    return jsonify(response)

@posts.route('/<id>', methods=['GET'])
def get_post(id):
    '''
    Get the post that corresponds to the id passed in 
    :id: String
    :return: json object
    '''

    post = db.get_post(id)
    return jsonify(post)

@posts.route('/', methods=['GET'])
def get_n_posts():

    start_time = request.args.get('startTime')
    start_post = request.args.get('startPost')
    num_posts = request.args.get('numPosts')
    response = {'errors': [], 'posts': []}

    if start_time == None:
        response['errors'].append('Missing startTime!')
    if start_post == None:
        response['errors'].append('Missing startPost!')
    if num_posts == None:
        response['errors'].append('Missing numPosts!')

    if len(response['errors']) == 0:
        response['posts'] = db.get_n_posts(int(start_post), int(start_time), int(num_posts))

    return jsonify(response)

@posts.route('/<id>', methods=['PUT'])
def update_post(id):
    pass

@posts.route('/<id>', methods=['DELETE'])
def delete_post(id):
    pass