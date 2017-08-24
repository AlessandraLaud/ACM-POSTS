# posts/controllers.py
# Written by Jeff Kaleshi

from flask import Blueprint, jsonify, request

posts = Blueprint('posts', __name__)

@posts.route('/new', methods=['POST'])
def add_post():
    pass

@posts.route('/<id>', methods=['GET'])
def get_post(id):
    pass

@posts.route('/<id>', methods=['PUT'])
def update_post(id):
    pass

@posts.route('/<id>', methods=['DELETE'])
def delete_post(id):
    pass