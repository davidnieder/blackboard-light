# -*- coding: utf-8 -*-

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(60))
    is_admin = db.Column(db.Boolean)

    def __init__(self, name, password, is_admin):
        self.name = name
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return '<User \'%s\'>' %self.name

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

def load_user(user_id):
    return User.query.get(int(user_id))

tag_lookups = db.Table('tag_lookups',
                db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('posts.id')))


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    #rendered_content = db.Column(db.Text)
    time = db.Column(db.DateTime)
    is_public = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='posts', uselist=False)

    tags = db.relationship('Tag', secondary=tag_lookups,
                backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, content, is_public, user, tags,
                 time=datetime.utcnow()):
        self.title = title
        self.content = content
        #self.rendered_content = self.render_post(content)
        self.is_public = is_public
        self.user = user
        self.tags = tags
        self.time = time

    def __repr__(self):
        return '<Post #%d>' %self.id

    def to_public_dict(self):
        taglist = [tag.name for tag in self.tags]
        return dict(id=self.id, title=self.title, content=self.content,
                    time=self.time, is_public=self.is_public,
                    user=self.user.name, tags=taglist)

    def update(self, title, content, is_public, taglist):
        self.title = title
        self.content = content
        #self.rendered_content = self.render_post(content)
        self.is_public = is_public
        self.tags = [Tag.query.filter_by(name=tag.name).first() \
                     or tag for tag in taglist]

#    def render_post(self):
#        post = self.content.replace('\r\n', '\n')
#        post = post.replace('\n', '<br>')
#        self.rendered_post = self.content


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag \'%s\'>' %self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    @classmethod
    def get_existing_tags(self, tag_list):
        ''' removes tags from tag_list that dont exist in the database '''
        existing_tags = []
        for tag in tag_list:
            et = Tag.query.filter_by(name=tag.name).first()
            if et and et not in existing_tags:
                existing_tags.append(et)
        return existing_tags

