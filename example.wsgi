# -*- coding: utf-8 -*-

import site
site.addsitedir('/var/www/blackboard-light')
site.addsitedir('/var/www/blackboard-light/venv/lib/python2.7/site-packages')

from config import config_map
from app import app_factory
application = app_factory(config_map['production'])
