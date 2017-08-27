# app/__init__.py
# Written by Jeff Kaleshi

from flask import Flask

from config import config
from .database import Database

db = Database()

def create_app(environment):
    '''
    App Factory
    :environment: server environment
    :return: Flask App
    '''
    app = Flask(__name__)
    app.config.from_object(config[environment])

    # initialize apps
    db.init_app(app)

    # import routes
    from .posts.controllers import posts
    app.register_blueprint(posts)

    from .uploads.controllers import uploads
    app.register_blueprint(uploads, url_prefix='/uploads')

    return app