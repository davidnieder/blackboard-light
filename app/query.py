# -*- coding: utf-8 -*-

from datetime import timedelta

from flask import current_app as app
from flask.ext.login import current_user

from .models import db, Post, User
from .forms import RequestArgs


class PostQuery(object):

    def __init__(self, query_args):
        self.query = Post.query
        self.query_args = query_args
        self.next_req_args = dict()
        self.per_page = app.config['POSTS_PER_PAGE']
        self.post_list = list()
        self.previous_page = 0
        self.current_page = 0
        self.next_page = 0
        self.results = 0
        self.total = 0
        self.has_more = False

    def fire(self):
        self._filter()
        self._paginate()
        return self

    def _paginate(self):
        page_no = self.query_args.page.data if self.query_args.page.data else 1
        pagination = self.query.paginate(page_no, self.per_page, False)
        self.post_list = pagination.items
        self.previous_page = pagination.prev_num
        self.current_page = pagination.page
        self.next_page = pagination.next_num if pagination.has_next else 0
        self.results = len(pagination.items)
        self.total = pagination.total
        self.has_more = pagination.has_next

    def _filter(self):
        # shortcuts
        query = self.query
        query_args = self.query_args

        # a not logged-in user can only see public posts
        if not current_user.is_authenticated():
            query = query.filter_by(is_public=True)

        # query for a particular post
        if self.query_args.postId.data:
            query = query.filter_by(id=query_args.postId.data)
            self.next_req_args['postId'] = query_args.postId.data

        # all posts with an id greater than x
        if self.query_args.sincePost.data:
            query = query.filter(Post.id>query_args.sincePost.data)
            self.next_req_args['sincePost'] = query_args.sincePost.data

        # all posts with an id smaller than x
        if self.query_args.beforePost.data:
            query = query.filter(Post.id<query_args.beforePost.data)
            self.next_req_args['beforePost'] = query_args.beforePost.data

        # exclude posts which are marked private
        if self.query_args.onlyPublicPosts.data is True:
            query = query.filter(Post.is_public == True)
            self.next_req_args['onlyPublicPosts'] = query_args.onlyPublicPosts.data

        # exclude posts which are marked public
        if self.query_args.onlyPrivatePosts.data is True:
            query = query.filter(Post.is_public == False)
            self.next_req_args['onlyPrivatePosts'] = query_args.onlyPrivatePosts.data

        # all posts from a specific user
        if self.query_args.user.data:
            user = User.query.filter_by(name=query_args.user.data).first()
            user_id = user.id if user else 0
            query = query.filter_by(user_id=user_id)
            self.next_req_args['user'] = query_args.user.data

        # all posts with certain tags, ignoring tags that don't exist
        if self.query_args.tags.data:
            self.next_req_args['tags'] = query_args.tags.query_string()
            for tag in query_args.tags.data:
                query = query.filter(Post.tags.any(name=tag.name))

        # all posts created since a given date, excluding posts from the date
        if self.query_args.since.data:
            date = query_args.since.data
            query = query.filter(Post.time >= date+timedelta(1))
            self.next_req_args['since'] = query_args.since.data.isoformat()

        # all posts created before a given date
        if self.query_args.before.data:
            query = query.filter(Post.time < query_args.before.data)
            self.next_req_args['before'] = query_args.before.data.isoformat()

        # all posts created on a specific date
        if self.query_args.createdOn.data:
            date = query_args.createdOn.data
            query = query.filter(Post.time >= date)
            query = query.filter(Post.time < date+timedelta(1))
            self.next_req_args['createdOn'] = date.isoformat()

        # order posts ascending if requested and descending by default
        if self.query_args.order.data == u'asc':
            query = query.order_by(Post.id.asc())
            self.next_req_args['order'] = u'asc'
        else:
            query = query.order_by(Post.id.desc())

        self.query = query
