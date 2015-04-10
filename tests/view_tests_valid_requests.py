# -*- coding: utf-8 -*-

import itertools
from datetime import date, timedelta

from app.blog import messages

from .view_tests_base import ViewTestsBase


class ViewTestsValid(ViewTestsBase):

    def populate_database(self):
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

        for post in self.posts:
            self.login(self.users[post[4]][0], self.users[post[4]][1])
            self.create_post(post[0], post[1], post[2], post[3])
        self.logout()

    # test index view #
    def test_index_view_get_empty_db(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue(messages.empty_database in resp.get_data())

    def test_index_view_query_posts(self):
        self.populate_database()
        # query index
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        for post in self.posts:
            if post[3] == 'y':
                self.assertTrue(self.post_in_response(post, resp))
            else:
                self.assertFalse(self.post_in_response(post, resp))

    def test_index_query_postid_arg(self):
        self.populate_database()
        # query single post
        resp = self.client.get('/?postId=2')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue(self.post_in_response(self.posts[1], resp))
        # query single private post
        resp = self.client.get('/?postId=1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertFalse(self.post_in_response(self.posts[1], resp))
        self.assertTrue(messages.empty_response in resp.get_data())

    def test_index_query_user_arg(self):
        self.populate_database()
        # query for user posts
        self.login('linus', 'vanPelt')
        resp = self.client.get('/?user=sally')
        for post in self.posts:
            if post[4] == 1:
                self.assertTrue(self.post_in_response(post, resp))
            else:
                self.assertFalse(self.post_in_response(post, resp))

    def test_index_query_greater_smaller_args(self):
        # query for post ids greater/smaller than
        self.populate_database()
        self.login('linus', 'vanPelt')
        resp = self.client.get('/?sincePost=6')
        for post in itertools.islice(self.posts, 0, 6):
            self.assertFalse(self.post_in_response(post, resp))
        for post in itertools.islice(self.posts, 6, None):
            self.assertTrue(self.post_in_response(post, resp))
        resp = self.client.get('/?sincePost=2&beforePost=5')
        for post in itertools.islice(self.posts, 0, 2):
            self.assertFalse(self.post_in_response(post, resp))
        for post in itertools.islice(self.posts, 2, 4):
            self.assertTrue(self.post_in_response(post, resp))
        for post in itertools.islice(self.posts, 4, None):
            self.assertFalse(self.post_in_response(post, resp))
        resp = self.client.get('/?beforePost=3&sincePost=7')
        for post in self.posts:
            self.assertFalse(self.post_in_response(post, resp))
        self.assertTrue(messages.empty_response in resp.get_data())

    def test_index_query_tags_arg(self):
        # query for tags
        self.populate_database()
        self.login('linus', 'vanPelt')
        resp = self.client.get('/?tags=muuusic')
        for post in self.posts:
            self.assertFalse(self.post_in_response(post, resp))
        self.assertTrue(messages.empty_response in resp.get_data())
        resp = self.client.get('/?tags=politics')
        for post in itertools.islice(self.posts, 0, 9):
            self.assertFalse(self.post_in_response(post, resp))
        self.assertTrue(self.post_in_response(self.posts[9], resp))
        resp = self.client.get('/?tags=politics,music')
        for post in self.posts:
            self.assertFalse(self.post_in_response(post, resp))
        resp = self.client.get('/?tags=music,video')
        for post in self.posts:
            if 'music' in post[2] and 'video' in post[2]:
                self.assertTrue(self.post_in_response(post, resp))
            else:
                self.assertFalse(self.post_in_response(post, resp))

    def test_index_query_older_younger_args(self):
        # query posts older/younger than date x
        self.populate_database()
        self.login('linus', 'vanPelt')
        resp = self.client.get('/?since='+(date.today()-timedelta(1)).isoformat())
        self.assertEqual(resp.status_code, 200)
        for post in itertools.islice(self.posts, 5, None):
            self.assertTrue(self.post_in_response(post, resp))
        resp = self.client.get('/?since='+date.today().isoformat())
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(messages.empty_response in resp.get_data())
        for post in self.posts:
            self.assertFalse(self.post_in_response(post, resp))
        resp = self.client.get('/?before='+(date.today()+timedelta(1)).isoformat())
        self.assertEqual(resp.status_code, 200)
        for post in itertools.islice(self.posts, 5, None):
            self.assertTrue(self.post_in_response(post, resp))
        resp = self.client.get('/?before='+date.today().isoformat())
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(messages.empty_response in resp.get_data())
        for post in self.posts:
            self.assertFalse(self.post_in_response(post, resp))

    def test_index_query_createdon_arg(self):
        # query posts created on a date x
        self.populate_database()
        resp = self.client.get('/?createdOn='+(date.today()-timedelta(1)).isoformat())
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(messages.empty_response in resp.get_data())
        for post in self.posts:
            self.assertFalse(self.post_in_response(post, resp))
        resp = self.client.get('/?cretedOn='+date.today().isoformat())
        for post in itertools.islice(post, 5, None):
            self.assertTrue(self.post_in_response(post,resp))

    def test_index_query_private_public_args(self):
        # filter for private/public posts
        self.populate_database()
        self.login('linus', 'vanPelt')
        resp = self.client.get('/?onlyPrivatePosts=true')
        self.assertEqual(resp.status_code, 200)
        for post in self.posts:
            if post[3] == 'y':
                self.assertFalse(self.post_in_response(post, resp))
            else:
                self.assertTrue(self.post_in_response(post, resp))
        resp = self.client.get('/?onlyPublicPosts=true')
        for post in self.posts:
            if post[3] == 'n':
                self.assertFalse(self.post_in_response(post, resp))
            else:
                self.assertTrue(self.post_in_response(post, resp))
        resp = self.client.get('/?onlyPublicPosts=true&onlyPrivatePosts=true')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(messages.empty_response in resp.get_data())

        self.logout()
        resp = self.client.get('/?onlyPrivatePosts=true')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(messages.empty_response in resp.get_data())

    def test_index_query_order_arg(self):
        # query with order argument
        self.populate_database()
        self.login('linus', 'vanPelt')
        resp = self.client.get('/?order=asc')
        self.assertEqual(resp.status_code, 200)
        for post in itertools.islice(self.posts, 0, 5):
            self.assertTrue(self.post_in_response(post, resp))
        resp = self.client.get('/?order=desc')
        self.assertTrue(resp.status_code, 200)
        for post in itertools.islice(self.posts, 5, None):
            self.assertTrue(self.post_in_response(post, resp))
        resp = self.client.get('/?order=ascc')
        self.assertEqual(resp.status_code, 400)
        resp = self.client.get('/?order=')
        self.assertEqual(resp.status_code, 200)
        for post in itertools.islice(self.posts, 5, None):
            self.assertTrue(self.post_in_response(post, resp))

    # test login view #
    def test_get_login_page(self):
        resp = self.client.get('/login')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')

    def test_valid_login(self):
        self.create_user('admin', 'strongpw', True)
        self.create_user('lucy', '1234', False)

        resp = self.login('admin', 'strongpw')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('logged in as <i>admin</i>' in resp.get_data())

        resp = self.login('lucy', '1234')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('logged in as <i>lucy</i>' in resp.get_data())

    # test logout view #
    def test_valid_logout(self):
        self.create_user('admin', 'strongpw', True)
        self.login('admin', 'strongpw')
        token = self.get_csrf_token()

        resp = self.client.get('/logout?csrfToken='+token, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(messages.user_logged_out in resp.get_data())

    # test new_post view #
    def test_newpost_view_valid_posts(self):
        self.create_user('charlie', 'brown', False)
        self.login('charlie', 'brown')
        resp = self.client.post('/newPost', follow_redirects=True, data=
                {'title':'a post','content':'with content','is_public':'y',
                 'csrf_token':self.get_csrf_token()})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue('a post' in resp.get_data())
        self.assertTrue('with content' in resp.get_data())
        self.assertTrue('tagged with' not in resp.get_data())

    def test_newpost_view_invalid_posts(self):
        # empty post body
        self.create_user('linus', 'vanPelt', False)
        self.login('linus', 'vanPelt')
        resp = self.client.post('/newPost', data={'title':'hello','content':'',
            'is_public':'y','csrf_token':self.get_csrf_token()})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue(messages.post_creation_error in resp.get_data())

    # test edit_post view #
    def test_editpost_view_valid_posts(self):
        self.create_user('lucy', 'vanPelt', False)
        self.login('lucy', 'vanPelt')
        self.create_post('hey', 'kikc teh bal, charlie', '', '0')
        resp = self.client.post('/editPost?postId=1', data={'title':'hey!',
                'content':'kick the ball, charlie','is_public':'','csrf_token':
                self.get_csrf_token()}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue(messages.post_edited in resp.get_data())
        self.assertTrue('hey!' in resp.get_data())
        self.assertTrue('kick the ball, charlie' in resp.get_data())

    def test_editpost_view_invalid_posts(self):
        # no post content
        self.create_user('lucy', 'vanPelt', False)
        self.login('lucy', 'vanPelt')
        self.create_post('hey', 'kick the ball, charlie', '', '0')
        resp = self.client.post('/editPost?postId=1', data={'title':'hey!',
                'content':'','is_public':'','csrf_token':self.get_csrf_token()})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue(messages.post_editing_error in resp.get_data())

    def test_editpost_view_edit_as_admin(self):
        self.create_user('lucy', 'vanPelt', False)
        self.create_user('charlie', 'brown', True)
        self.login('lucy', 'vanPelt')
        self.create_post('hey', 'kick the ball, charlie', '', '0')
        self.login('charlie', 'brown')
        resp = self.client.post('/editPost?postId=1', data={'title':'hey',
                'content':'no i won\'t','is_public':'','csrf_token':
                self.get_csrf_token()}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue(messages.post_edited in resp.get_data())
        self.assertTrue('no i won\'t' in resp.get_data())

    # test delete_post view #
    def test_deletepost_view_valid_requests(self):
        self.create_user('peppermint', 'patty', False)
        self.login('peppermint', 'patty') 
        self.create_post('First', 'Post', '', '1')
        resp = self.client.get('/deletePost?postId=1&csrfToken='+\
                self.get_csrf_token(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue(messages.post_deleted in resp.get_data())

    def test_deletepost_view_delete_as_admin(self):
        self.create_user('lucy', 'vanPelt', False)
        self.create_user('charlie', 'brown', True)
        self.login('lucy', 'vanPelt')
        self.create_post('hey', 'kick the ball, charlie', '', 'y')
        self.login('charlie', 'brown')
        resp = self.client.get('/deletePost?postId=1&csrfToken='+\
                self.get_csrf_token(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')
        self.assertTrue(messages.post_deleted in resp.get_data())
