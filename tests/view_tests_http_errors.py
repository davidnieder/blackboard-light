# -*- coding: utf-8 -*-

from app.blog import messages

from .tests_base import TestsBase


class ViewTestsHTTPErrors(TestsBase):

    def test_index_wrong_method(self):
        # invalid request method
        resp = self.client.post('/', data={'csrf_token':self.get_csrf_token()})
        self.assertEqual(resp.status_code, 405)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Method Not Allowed' in resp.get_data())

    def test_index_malformed_query_args(self):
        # postId
        resp = self.client.get('/?postId=0')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())
        resp = self.client.get('/?postId=abc')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())
        # sincePost
        resp = self.client.get('/?sincePost=0')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())
        resp = self.client.get('/?sincePost=abc')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())
        # beforePost
        resp = self.client.get('/?beforePost=0')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())
        resp = self.client.get('/?beforePost=abc')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())
        # page
        resp = self.client.get('/?page=0')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())
        resp = self.client.get('/?page=abc')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())
        # order
        resp = self.client.get('/?order=abc')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())
        # since
        resp = self.client.get('/?since=13042015')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())
        # before
        resp = self.client.get('/?before=1234')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())
        # createdOn
        resp = self.client.get('/?createdOn=abcdefg')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())

    def test_login_view_http_errors(self):
        # post request without csrf token
        resp = self.client.post('/login')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())

    def test_logout_view_http_errors(self):
        # test invalid request method
        resp = self.client.post('/logout',
                data={'csrf_token':self.get_csrf_token()})
        self.assertEqual(resp.status_code, 405)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Method Not Allowed' in resp.get_data())

        # get request, unauthorized
        resp = self.client.get('/logout?csrfToken=%s' %self.get_csrf_token())
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Unauthorized' in resp.get_data())

        # test request without csrf token
        self.create_user('charlie', 'drowssap', False)
        self.login('charlie', 'drowssap')
        resp = self.client.get('/logout')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())

    def test_newpost_view_http_errors(self):
        # post request without csrf token
        resp = self.client.post('/newPost')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())

        # get request unauthorized
        resp = self.client.get('/newPost')
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Unauthorized' in resp.get_data())

        # post request unauthorized
        resp = self.client.post('/newPost',
                data={'csrf_token':self.get_csrf_token()})
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Unauthorized' in resp.get_data())

    def test_editpost_http_errors(self):
        # post request without csrf_token
        resp = self.client.post('/editPost')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())

        # get request, unauthorized
        resp = self.client.get('/editPost')
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Unauthorized' in resp.get_data())

        # post request, unauthorized
        resp = self.client.post('/editPost',
                data={'csrf_token':self.get_csrf_token()})
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Unauthorized' in resp.get_data())

        # get request without query args
        self.create_user('admin', '1234', True)
        self.login('admin', '1234')
        resp = self.client.get('/editPost')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())

        # post request without query args
        resp = self.client.post('/editPost',
                data={'csrf_token':self.get_csrf_token()})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())

        # get request, malformed postId
        resp = self.client.get('/editPost?postId=0g')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())

        # post request, malformed postId
        resp = self.client.post('/editPost?postId= ',
                data={'csrf_token':self.get_csrf_token()})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())

        # get request, not existing post
        resp = self.client.get('/editPost?postId=1')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Not Found' in resp.get_data())

        # post request, not existing post
        resp = self.client.post('/editPost?postId=9',
                data={'csrf_token':self.get_csrf_token()})
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Not Found' in resp.get_data())

    def test_editpost_view_insufficient_rights(self):
        self.create_user('lucy', 'vanPelt', False)
        self.create_user('charlie', 'brown', False)
        self.login('lucy', 'vanPelt')
        self.create_post('hey', 'kick the ball, charlie', '', '0')
        self.login('charlie', 'brown')
        resp = self.client.post('/editPost?postId=1', data={'title':'hey',
                'content':'no i won\'t','is_public':'','csrf_token':
                self.get_csrf_token()})
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Forbidden' in resp.get_data())

    def test_deletepost_http_errors(self):
        # invalid request method
        resp = self.client.post('/deletePost',
            data={'csrf_token':self.get_csrf_token()})
        self.assertEqual(resp.status_code, 405)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Method Not Allowed' in resp.get_data())

        # get request, unauthorized
        resp = self.client.get('/deletePost?postId=1&csrfToken='+\
                self.get_csrf_token())
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Unauthorized' in resp.get_data())

        # get request without postId
        self.create_user('admin', '1234', True)
        self.login('admin', '1234')
        resp = self.client.get('/deletePost?csrfToken='+\
                self.get_csrf_token())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())

        # get request without csrf token
        self.create_post('#1', 'first!', '', '')
        resp = self.client.get('/deletePost?postId=1')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())

        # get request with malformed postId argument
        resp = self.client.get('/deletePost?postId=abc&csrfToken='+\
                self.get_csrf_token())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Bad Request' in resp.get_data())

        # get request, not existing post
        resp = self.client.get('/deletePost?postId=2&csrfToken='+\
                self.get_csrf_token())
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Not Found' in resp.get_data())

    def test_deletepost_view_insufficient_rights(self):
        self.create_user('lucy', 'vanPelt', True)
        self.create_user('charlie', 'brown', False)
        self.login('lucy', 'vanPelt')
        self.create_post('hey', 'kick the ball, charlie', '', 'y')
        self.login('charlie', 'brown')
        resp = self.client.get('/deletePost?postId=1&csrfToken='+\
                self.get_csrf_token())
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('Forbidden' in resp.get_data())
