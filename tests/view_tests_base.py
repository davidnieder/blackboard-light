# -*- coding: utf-8 -*-

import unittest

from bs4 import BeautifulSoup
from flask import current_app

from app.models import db, User


class ViewTestsBase(unittest.TestCase):
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
        content = '<div class="post-content"><p>%s</div>' %post[1]
        return title in response.get_data() and content in response.get_data()

