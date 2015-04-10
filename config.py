# -*- coding: utf-8 -*-


class Config(object):
    DEBUG = False
    TESTING = False
    POSTS_PER_PAGE = 3


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'development_secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blackboard_development.db'


class TestingConfig(Config):
    TESTING = False # suppress extension testing behavior, esp. flask-login
    SECRET_KEY = 'testing_secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
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
