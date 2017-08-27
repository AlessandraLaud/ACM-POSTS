# Written by Jeff Kaleshi

import os

class Config:
    DB_URI = os.environ['DB_URI']
    DB_PORT = int(os.environ['DB_PORT'])
    DB_NAME = os.environ['DB_NAME']
    UPLOAD_PATH = os.environ['UPLOAD_PATH']
    
    
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}