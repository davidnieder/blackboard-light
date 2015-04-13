# -*- coding: utf-8 -*-

import json
import itertools

from .tests_base import TestsApiBase


class ApiTests(TestsApiBase):

    # test api invalid request methods
    def test_posts_invalid_methods(self):
        resp = self.client.put('/api/posts')
        self.assertEqual(resp.status_code, 400)
        resp = self.client.post('/api/posts')
        self.assertEqual(resp.status_code, 400)

    # test /api/posts GET
    def test_posts_get_empty_db(self):
        resp = self.client.get('/api/posts')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'application/json')
        data = json.loads(resp.get_data())
        self.assertEqual(data.get('postAmount'), 0)
        self.assertEqual(data.get('postList'), [])
        self.assertEqual(data.get('hasMore'), False)

    def test_posts_get(self):
        self.populate_database()
        self.login('sally', 'brown')
        resp = self.client.get('/api/posts')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.get_data())
        self.assertEqual(data.get('postAmount'), 5) # limit defaults to 5
        self.assertTrue(data.get('hasMore'))
        for post in itertools.islice(self.posts, 0, 5):
            self.assertFalse(self.post_in_response(post, resp.get_data()))
        for post in itertools.islice(self.posts, 5, None):
            self.assertTrue(self.post_in_response(post, resp.get_data()))

        # limit=10
        resp = self.client.get('/api/posts?limit=10')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.get_data())
        self.assertEqual(data.get('postAmount'), 10)
        self.assertFalse(data.get('hasMore'))
        for post in self.posts:
            self.assertTrue(self.post_in_response(post, resp.get_data()))

    # test DELETE errors
    def test_posts_delete_http_errors(self):
        self.populate_database(3)
        # unauthorized
        resp = self.client.delete('/api/posts?csrfToken=%s' %self.get_csrf_token())
        self.assertEqual(resp.status_code, 401)
        self.assertTrue('Unauthorized' in resp.get_data())
        # without csrf token
        self.login('linus', 'vanPelt')
        resp = self.client.delete('/api/posts')
        self.assertEqual(resp.status_code, 400)
        self.assertTrue('Bad Request' in resp.get_data())
        # malformed post id
        resp = self.client.delete('api/posts?csrfToken=%s&postId=abc'
                %self.get_csrf_token())
        self.assertEqual(resp.status_code, 400)
        self.assertTrue('Bad Request' in resp.get_data())
        # not existing post
        resp = self.client.delete('api/posts?csrfToken=%s&postId=11'
                %self.get_csrf_token())
        self.assertEqual(resp.status_code, 404)
        self.assertTrue('Not Found' in resp.get_data())
        # insufficient rights
        resp = self.client.delete('api/posts?csrfToken=%s&postId=3'
                %self.get_csrf_token())
        self.assertEqual(resp.status_code, 403)
        self.assertTrue('Forbidden' in resp.get_data())

    # test DELETE valid request
    def test_posts_delete_valid_request(self):
        self.populate_database(1)
        self.login('linus', 'vanPelt')
        resp = self.client.delete('api/posts?csrfToken=%s&postId=1'
                %self.get_csrf_token())
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(json.loads(resp.get_data()).get('success'))
