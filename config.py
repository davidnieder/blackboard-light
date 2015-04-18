# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))
dbdir = basedir + '/database'


class Config(object):
    DEBUG = False
    TESTING = False
    POSTS_PER_PAGE = 5


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'development_secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + dbdir + '/development.db'
    WHOOSH_BASE = dbdir + '/search_index_development'


class TestingConfig(Config):
    TESTING = False # suppress extension testing behavior, esp. flask-login
    SECRET_KEY = 'testing_secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WHOOSH_BASE =  dbdir + '/search_index_testing'
    POSTS_PER_PAGE = 5

try:
    from config_production import ProductionConfig
except ImportError:
    class ProductionConfig(Config):
        pass


config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
