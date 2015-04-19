#!venv/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from argparse import ArgumentParser
from getpass import getpass
import code
import sys

from app import app_factory
from config import config_map
from app.models import db, User, Post


def toUnicode(bytestr, encoding=sys.stdin.encoding):
    return bytestr.decode(encoding)

def runserver(args):
    app = app_factory(config=config_map[args.config])
    app.run()

def runtests(args):
    import tests, coverage
    c = coverage.coverage(source=['app'])
    c.start()
    app = app_factory(config=config_map['testing'])
    with app.app_context():
        tests.run(args.verbosity)
    if args.coverage:
        c.report()

def createdb(args):
    app = app_factory(config=config_map[args.config])
    with app.app_context():
        db.create_all()

def adduser(args):
    password1 = getpass('password: ')
    password2 = getpass('confirm: ')
    if password1 != password2:
        sys.exit('error: passwords do no match')
    with app_factory(config=config_map[args.config]).app_context():
        if User.query.filter_by(name=args.name).first() is not None:
            sys.exit('error: user name already exists')
        user = User(args.name, toUnicode(password1), args.is_admin)
        db.session.add(user)
        db.session.commit()

def deluser(args):
    with app_factory(config=config_map[args.config]).app_context():
        user = User.query.filter_by(name=args.name).first()
        if user is None:
            sys.exit('No such user: %s' %args.name)
        elif Post.query.filter_by(user=user).first() is not None:
            sys.exit('User %s has posts. Can not delete.' %args.name)
        else:
            db.session.delete(user)
            db.session.commit()

def listusers(args):
    with app_factory(config=config_map[args.config]).app_context():
        for user in User.query.all():
            admin = '*' if user.is_admin else ' '
            print('(%i)%s %s' %(user.id, admin, user.name))
        print('(* marked users have admin rights)')

def shell(args):
    app = app_factory(config=config_map[args.config])
    with app.app_context():
        code.interact(banner='blackboard shell, imported into scope: app, db',
            local=dict(app=app, db=db))

def main():
    arg_parser = ArgumentParser()
    sub_parsers = arg_parser.add_subparsers()

    # runserver command
    cmd_runserver = sub_parsers.add_parser('runserver',
            help='runs the flask development server')
    cmd_runserver.add_argument('--config', default='default',
            help='config to use')
    cmd_runserver.set_defaults(func=runserver)

    # runtests command
    cmd_runtests = sub_parsers.add_parser('runtests',
            help='runs the test suite')
    cmd_runtests.add_argument('--verbosity', default=1, type=int,
            help='set unittest output verbosity, default: 1')
    cmd_runtests.add_argument('--with-coverage', action='store_true',
            dest='coverage', help='print test coverage report')
    cmd_runtests.set_defaults(func=runtests)

    # createdb command
    cmd_createdb = sub_parsers.add_parser('createdb',
            help='creates the application database')
    cmd_createdb.add_argument('--config', default='default',
            help='config to use')
    cmd_createdb.set_defaults(func=createdb)

    # adduser command
    cmd_adduser = sub_parsers.add_parser('adduser',
            help='adds a user to the database')
    cmd_adduser.add_argument('--name', required=True, type=lambda s:toUnicode(s),
            help='the user name')
    cmd_adduser.add_argument('--is-admin', action='store_true',
            help='give admin rights to the new user')
    cmd_adduser.add_argument('--config', default='default',
            help='config to use')
    cmd_adduser.set_defaults(func=adduser)

    # deluser command
    cmd_deluser = sub_parsers.add_parser('deluser',
            help='removes a user from the database')
    cmd_deluser.add_argument('--name', required=True, type=lambda s:toUnicode(s),
            help='the user name')
    cmd_deluser.add_argument('--config', default='default',
            help='config to use')
    cmd_deluser.set_defaults(func=deluser)

    # listusers command
    cmd_listusers = sub_parsers.add_parser('listusers',
            help='lists all users that are in the database')
    cmd_listusers.add_argument('--config', default='default',
            help='config to use')
    cmd_listusers.set_defaults(func=listusers)

    # shell command
    cmd_shell = sub_parsers.add_parser('shell',
            help='runs a shell inside application context')
    cmd_shell.add_argument('--config', default='default',
            help='config to use')
    cmd_shell.set_defaults(func=shell)

    args = arg_parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
