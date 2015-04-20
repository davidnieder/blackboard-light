# -*- coding: utf-8 -*-

from config import Config, dbdir


class ProductionConfig(Config):
    SECRET_KEY = 'not-very-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + dbdir + '/blackboard-light.db'
    WHOOSH_BASE = dbdir + '/search_index'
