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
        self.assertEqual(resp.mimetype, 'application/json')
        data = json.loads(resp.get_data())
        self.assertEqual(data.get('postAmount'), 5) # limit defaults to 5
        self.assertTrue(data.get('hasMore'))
        for post in itertools.islice(self.posts, 0, 5):
            self.assertFalse(self.post_in_json_response(post, resp))
        for post in itertools.islice(self.posts, 5, None):
            self.assertTrue(self.post_in_json_response(post, resp))
        # limit=10
        resp = self.client.get('/api/posts?limit=10')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'application/json')
        data = json.loads(resp.get_data())
        self.assertEqual(data.get('postAmount'), 10)
        self.assertFalse(data.get('hasMore'))
        for post in self.posts:
            self.assertTrue(self.post_in_json_response(post, resp))
        # renderPosts
        resp = self.client.get('/api/posts?renderPosts=false')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'application/json')
        data = json.loads(resp.get_data())
        self.assertEqual(data.get('postAmount'), 5)
        self.assertTrue(data.get('hasMore'))
        for post in itertools.islice(self.posts, 0, 5):
            self.assertFalse(self.post_in_json_response(post, resp))
        for post in itertools.islice(self.posts, 5, None):
            self.assertTrue(self.post_in_json_response(post, resp))
        resp = self.client.get('/api/posts?renderPosts=true')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'application/json')
        data = json.loads(resp.get_data())
        self.assertEqual(data.get('postAmount'), 5)
        self.assertTrue(data.get('hasMore'))
        for post in itertools.islice(self.posts, 0, 5):
            self.assertFalse(self.rendered_post_in_json_response(post, resp))
        for post in itertools.islice(self.posts, 6, None):
            self.assertTrue(self.rendered_post_in_json_response(post, resp))

    # test DELETE errors
    def test_posts_delete_http_errors(self):
        self.populate_database(3)
        # unauthorized
        data = json.dumps(dict(csrfToken=self.get_csrf_token(), postId=1))
        resp = self.client.delete('/api/posts', data=data,
                content_type='application/json')
        self.assertEqual(resp.status_code, 401)
        self.assertTrue('Unauthorized' in resp.get_data())
        # without csrf token
        self.login('linus', 'vanPelt')
        data = json.dumps(dict(postId=1))
        resp = self.client.delete('/api/posts', data=data,
                content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertTrue('Bad Request' in resp.get_data())
        # malformed post id
        data = json.dumps(dict(csrfToken=self.get_csrf_token(), postId='abc'))
        resp = self.client.delete('/api/posts', data=data,
                content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertTrue('Bad Request' in resp.get_data())
        # no post id
        data = json.dumps(dict(csrfToken=self.get_csrf_token()))
        resp = self.client.delete('/api/posts', data=data,
                content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertTrue('Bad Request' in resp.get_data())
        # not existing post
        data = json.dumps(dict(csrfToken=self.get_csrf_token(), postId=4))
        resp = self.client.delete('/api/posts', data=data,
                content_type='application/json')
        self.assertEqual(resp.status_code, 404)
        self.assertTrue('Not Found' in resp.get_data())
        # insufficient rights
        data = json.dumps(dict(csrfToken=self.get_csrf_token(), postId=3))
        resp = self.client.delete('/api/posts', data=data,
                content_type='application/json')
        self.assertEqual(resp.status_code, 403)
        self.assertTrue('Forbidden' in resp.get_data())

    # test DELETE valid request
    def test_posts_delete_valid_request(self):
        self.populate_database(1)
        self.login('linus', 'vanPelt')
        data = json.dumps(dict(postId=1, csrfToken=self.get_csrf_token()))
        resp = self.client.delete('/api/posts', data=data,
                content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(json.loads(resp.get_data()).get('success'))

