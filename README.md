### about
blackboard-light is a simple, [flask](http://flask.pocoo.org/) powered blog engine. looks like [this](https://github.com/davidnieder/blackboard-light/raw/master/screenshot.png).

### requirements
python2 (only tested with v2.7), virtualenv

### setup development environment
```bash
# clone this repo:
$ git clone https://github.com/davidnieder/blackboard-light.git
$ cd blackboard-light/
# create the python environment:
$ virtualenv venv/
$ venv/bin/pip install -r requirements.txt
# run the test suite:
$ ./manager.py runtests
> ....
> ok
# create the database and your first user:
$ ./manager.py createdb --config development
$ ./manager.py adduser --config development --name david --is-admin
# run the development server:
$ ./manager.py runserver --config development
```

### installation (on debian+apache+mod_wsgi)
```bash
# clone this repo:
$ git clone https://github.com/davidnieder/blackboard-light.git
$ cd blackboard-light/
# create the python environment:
$ virtualenv venv/
$ venv/bin/pip install -r requirements.txt
# run the testsuite:
$ ./manager.py runtests
> ....
> ok
# configuration:
$ cp example.config.py config_production.py
# set the SECRET_KEY in config_production.py!
# give the wsgi process write access to database/:
$ chown -R www-data.www-data database/
# create the database and your first user:
$ ./manager.py createdb
$ ./manager.py adduser --name david --is-admin
# apache config:
$ cp example.wsgi blackboard-light.wsgi
$ cp example.vhost /etc/apache2/sites-available/blackboard-light
# adjust the wsgi/vhost file to your paths/apache config
# enable the vhost
$ cd /etc/apache2/sites-enabled/
$ ln -s ../sites-available/blackboard-light blackboard-light
# restart apache:
$ apachectl configtest
$ apachectl restart
```

### used libs/frameworks
* flask, werkzeug, jinja2
* wtforms, flask-wtforms
* sqlalchemy, flask-sqlalchemy
* whoosh, flask-whooshalchemy
* flask-login
* beautifulsoup
* coverage
* jquery
* skeleton.css, normalize.css

