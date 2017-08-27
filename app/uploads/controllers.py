# uploads/controllers.py
# Written by Alessandra Laudando
import os

from flask import Blueprint, current_app, send_from_directory

uploads = Blueprint('uploads', __name__)

@uploads.route('/<path:filename>')
def get_file(filename):
    '''
    Gets file from uploads directory 
    :filename: String
    :return: {}
    '''
    response = send_from_directory(
        current_app.config['UPLOAD_PATH'], filename)

    return response