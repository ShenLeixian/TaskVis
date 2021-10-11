import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 9999
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very_secret_key'
    # DATABASE_URI = 'admin:9980206@localhost/viznet'
    # DATABASE_URI = 'postgres:1111aaaa@192.168.10.172/viznet'
    # DATABASE_URI = 'postgres:1111aaaa@localhost/viznet'
    DATABASE_URI = 'postgres:autovis_123@localhost/viznet'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%s?client_encoding=utf8' % DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SITE_URL = 'OMITTED'
    DATABASE_URI = 'postgres:7sQ6fhOEQT4f@localhost/viznet'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%s?client_encoding=utf8' % DATABASE_URI    
