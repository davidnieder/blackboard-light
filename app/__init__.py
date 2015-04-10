# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.wtf.csrf import CsrfProtect

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
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.filters['datetime'] = lambda(o):o.strftime \
        ('%d.%m.%y - %H:%M utc') if hasattr(o,'strftime') else o
    app.jinja_env.filters['date'] = lambda(o):o.strftime \
        ('%B %d, %Y') if hasattr(o,'strftime') else o
    
    # blueprints
    from blog import blog
    app.register_blueprint(blog)

    return app
