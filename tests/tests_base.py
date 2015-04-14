# -*- coding: utf-8 -*-

import unittest
import json
import itertools

from bs4 import BeautifulSoup
from flask import current_app

from app.models import db, User


class TestsBase(unittest.TestCase):
    def setUp(self):
        self.client = current_app.test_client()
        self.posts_per_page = current_app.config.get('POSTS_PER_PAGE')
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def get_csrf_token(self):
        resp = self.client.get('/')
        s = BeautifulSoup(resp.get_data())
        return s.find('meta', attrs={'name': 'csrf_token'}).attrs['value']

    def login(self, user, password):
        token = self.get_csrf_token()
        return self.client.post('/login', follow_redirects=True,
            data={'name':user,'password':password,'csrf_token':token})

    def logout(self):
        return self.client.get('/logout?csrfToken='+self.get_csrf_token())

    def create_post(self, title, content, tags, is_public):
        token = self.get_csrf_token()
        return self.client.post('/newPost', follow_redirects=True,
            data={'title':title,'content':content,'tags':tags,
                  'is_public':is_public,'csrf_token':token})

    def create_user(self, name, password, is_admin):
        user = User(name, password, is_admin)
        db.session.add(user)
        db.session.commit()

    def post_in_response(self, post, response):
        title = '<header><h4>%s</h4></header>' %post[0]
        content = '<div class="post-content">%s</div>' %post[1]
        return title in response.get_data() and content in response.get_data()

    def populate_database(self, post_amount=10):
        self.users = [
            # name,     password,   admin
            ['linus',   'vanPelt',  False],
            ['sally',   'brown',    False]]
        self.posts = [
            # title,    content,        tags,           public, user
            ['Post#1',  'first post',   'text',         'n',    0],
            ['Post#2',  'second post',  'music',        'y',    0],
            ['Post#3',  'third post',   'video',        'n',    1],
            ['Post#4',  'fourth post',  'music,video',  'n',    0],
            ['Post#5',  'fifth post',   '',             'y',    0],
            ['Post#6',  'sixth post',   'text,poetry',  'n',    1],
            ['Post#7',  'seventh post', '',             'n',    1],
            ['Post#8',  'eighth post',  'video',        'y',    1],
            ['Post#9',  'ninth post',   'video,music',  'y',    0],
            ['Post#10', 'tenth post',   'politics',     'y',    1]]

        for user in self.users:
            self.create_user(user[0], user[1], user[2])

        for post in itertools.islice(self.posts, 0, post_amount):
            self.login(self.users[post[4]][0], self.users[post[4]][1])
            self.create_post(post[0], post[1], post[2], post[3])
        self.logout()

class TestsApiBase(TestsBase):

    def get_csrf_token(self):
        resp = self.client.get('/api/posts')
        return json.loads(resp.get_data()).get('csrfToken')

    def post_in_json_response(self, post, response):
        post_list = json.loads(response.get_data()).get('postList')
        for p in post_list:
            if post[0] == p.get('title') and post[1] == p.get('content'):
                return True
        return False

    def rendered_post_in_json_response(self, post, response):
        post_list = json.loads(response.get_data()).get('postList')
        title = '<header><h4>%s</h4></header>' %post[0]
        content = '<div class="post-content">%s</div>' %post[1]
        for post in post_list:
            if title in post and content in post:
                return True
        return False

