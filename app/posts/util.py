# posts/util.py
# Written by Alessandra Laudando

import os
import hashlib
from datetime import date
from time import time

from flask import current_app
from werkzeug.utils import secure_filename

from app import db

IMAGE_EXTENSIONS = [
    'png',
    'jpg',
    'jpeg',
    'gif',
]

DOCUMENT_EXTENSIONS = [
    'text',
    'pdf',
    'doc',
    'xls',
    'ppt',
]

def get_post_from_form(form):
    '''
        Retrieve the post from the form
        :form: MultiDict
        :return: {}
    '''
    post = {
        'body': form['body'],
        'author': form['author'],
        'title': form['title'],
        'type': form['type'],  
    }

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

def valid_file(filename, extensions):
    '''
        Checks if the file extension is valid
        :filename: String
        :extensions: [str, str, ...]
        :return: boolean
    '''
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions

def validate_form(form):
    '''
        Checks if the form contains the required fields
        :form: MultiDict
        :return: String
    '''

    message = ''
    if 'body' not in form or 'title' not in form or 'type' not in form:
        message = 'One or more required fields are missing!'

    return message

def validate_files(files, file_type, allowed_extensions):
    '''
        Checks if files is valid based on the 
        file extension type passed in
        :files: MultiDict
        :file_type: String
        :allowed_extensions: [str, str, ...]
        :return: String
    '''

    message = ''
    for file in files:
        if not valid_file(file.filename, allowed_extensions):
            files_valid = False
            message = 'One or more {} have an invalid extension!'.format(file_type)
            break
    
    return message

def save_files(files, folder_name, username):
    '''
        Saves the files
        :files: MultiDict
        :folder_name: String
        :username: String
        :return: [str, str, ...]
    '''
    
    all_files_valid = True
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

    