# posts/util.py
# Written by Alessandra Laudando

import os
import hashlib
from datetime import date
from time import time

from flask import current_app, url_for
from werkzeug.utils import secure_filename

from app import db

def get_post_with_urls(post):
    '''
    Get the post with image/docuents's corresponding urls
    :post: {}
    :return: {}
    '''
    image_paths = post.images
    document_paths = post.documents

    if image_paths:
        images = []
        for path in image_paths:
            images.append(url_for('uploads.get_file', filename=path, _external=True))
        
        documents = []
        for path in document_paths:
            documents.append(url_for('uploads.get_file', filename=path, _external=True))
        
        post.documents = documents
        post.images = images

    return post

def generate_folder_path(folder_name, username):
    '''
        Generate the folder path based on the users name, 
        current date, upload path, and current time  
        :folder_name: String
        :username: String
        :return: String
    '''
    username_hash = hashlib.md5(username.encode()).hexdigest()
    today = date.today()
    path = os.path.join(
        str(today.year),
        str(today.month),
        str(today.day),
        str(int(time())),
        username_hash,
        folder_name
        )
    return path


def save_files(files, folder_name, username):
    '''
        Saves the files
        :files: MultiDict
        :folder_name: String
        :username: String
        :return: [str, str, ...]
    '''
    images = []
    
    if len(files) > 0:
        rel_folder_path = generate_folder_path(folder_name, username)
        abs_folder_path = os.path.join(
            current_app.config['UPLOAD_PATH'], rel_folder_path)

        if not os.path.exists(abs_folder_path):
            os.makedirs(abs_folder_path)

        for file in files:
            filename = secure_filename(file.filename)
            rel_file_path = os.path.join(rel_folder_path, filename)
            abs_file_path = os.path.join(abs_folder_path, filename)
            file.save(abs_file_path)
            images.append(rel_file_path)
    
    return images

def create_posts_dictionary(posts):
    '''
        Takes in a list of posts and returns a list
        of dictionaries containing post information
        :posts: [post, post, ...]
        :return: [{}, {}, ...]
    '''
    posts_data = []
    for post in posts:
        post = get_post_with_urls(post)
        posts_data.append(post.get_json())

    return posts_data


def save_post(post_data):
    '''
    Save the post
    :post_data: {}
    :return: {}
    '''
    image_paths = []
    document_paths = []

    if post_data['images'] != None:
        image_paths = save_files(
            post_data['images'], 'images', post_data['author'])
    if post_data['documents'] != None:
        document_paths = save_files(
            post_data['documents'], 'documents', post_data['author'])

    post_data['images'] = image_paths
    post_data['documents'] = document_paths
    post_data['time'] = int(time())

    post = db.add_post(post_data)

    return post
