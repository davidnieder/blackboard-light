# -*- coding: utf-8 -*-

from flask.views import View
from werkzeug.datastructures import MultiDict
from flask import jsonify, request, abort, render_template
from flask.ext.login import login_required, current_user
from flask.ext.wtf.csrf import validate_csrf, generate_csrf

from ..forms import RequestArgs
from ..query import PostQuery
from ..models import Post, db


class BaseView(View):
    methods = ['GET']

    def __init__(self):
        self.request_args = RequestArgs(formdata=request.args)
        self.request_data = RequestArgs(formdata=MultiDict(request.get_json()))
        self.response_data = dict()

        if not self.request_args.validate():
            abort(400)

        if request.method in ['DELETE']:
            if not validate_csrf(self.request_data.csrfToken.data):
                abort(400)

        self.response_data.update(csrfToken=generate_csrf())

    def dispatch_request(self):
        method = getattr(self, request.method.lower(), None)
        if method is not None:
            r = method()

        return jsonify(self.response_data)


class Posts(BaseView):

    def get(self):
        query = PostQuery(query_args=self.request_args)
        query.fire()

        if self.request_args.renderPosts.data:
            post_list = list()
            for post in query.post_list:
                template = render_template('post.html', post=post.to_public_dict())
                post_list.append(template)
        else:
            post_list = [post.to_public_dict() for post in query.post_list]

        self.response_data.update(postList=post_list)
        self.response_data.update(postAmount=query.results)
        has_more = query.has_more
        self.response_data.update(hasMore=has_more)

class DeletePost(BaseView):
    methods = ['DELETE']
    decorators = [login_required]

    def delete(self):
        if not self.request_data.postId.data:
            abort(400)
        post = Post.query.get_or_404(self.request_data.postId.data)
        if post.user_id != current_user.id and not current_user.is_admin:
            abort(403)

        db.session.delete(post)
        db.session.commit()
        self.response_data.update(success=True)

