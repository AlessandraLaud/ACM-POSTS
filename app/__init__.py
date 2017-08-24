# app/__init__.py
# Written by Jeff Kaleshi

from flask import Flask

from config import config
from .posts.controllers import posts

def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(config[environment])

    app.register_blueprint(posts)
    return app