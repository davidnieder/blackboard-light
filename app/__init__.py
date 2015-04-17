# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.wtf.csrf import CsrfProtect

import jinja
from models import db, load_user


def app_factory(config):
    # create app
    app = Flask(__name__)
    app.config.from_object(config)

    # database
    db.init_app(app)

    # flask-login
    login_manager = LoginManager(app)
    login_manager.user_loader(load_user)

    # flask-wtf csrf protection
    CsrfProtect(app)

    # jinja2 config
    jinja.init_app(app)

    # blueprints
    from blog import blog
    app.register_blueprint(blog)

    from api import api
    app.register_blueprint(api, url_prefix='/api')

    return app
