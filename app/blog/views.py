# -*- coding: utf-8 -*-

from datetime import timedelta

from flask import render_template, request, redirect, url_for, abort
from flask import jsonify, flash, get_flashed_messages
from flask.views import View
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import current_user
from flask.ext.wtf.csrf import validate_csrf

from ..forms import LoginForm, PostForm, RequestArgs
from ..models import db, User, Post, Tag
from ..query import PostQuery
from . import messages


class BaseView(View):
    methods = ['GET']

    def __init__(self):
        self.template = 'index.html'
        self.request_args = RequestArgs(formdata=request.args)
        self.request_data = request.form
        self.response_data = dict()

        if not self.request_args.validate():
            abort(400)

    def dispatch_request(self):
        # if a derived class provides a method for the current request
        # type (get(), post(), etc), call it
        method = getattr(self, request.method.lower(), None)
        if method is not None:
            r = method()
            # if method() returns something, assume it is a respond
            if r is not None:
                return r

        return render_template(self.template, **self.response_data)


class Index(BaseView):
    def __init__(self):
        BaseView.__init__(self)

    def get(self):
        query = PostQuery(query_args=self.request_args)
        query.fire()

        self.response_data['post_list'] = [post.to_public_dict() \
                                           for post in query.post_list]
        self.response_data['prev_page'] = query.previous_page
        self.response_data['current_page'] = query.current_page
        self.response_data['next_page'] = query.next_page
        self.response_data['query_args'] = query.next_req_args

        if query.total == 0 and Post.query.count() == 0:
            flash(messages.empty_database, 'info')
        elif query.total == 0:
            flash(messages.empty_response, 'info')


class Login(BaseView):
    methods = ['GET', 'POST']

    def __init__(self):
        BaseView.__init__(self)
        self.template = 'login.html'
        self.form = LoginForm()

    def get(self):
        self.response_data['login_form'] = self.form

    def post(self):
        if self.form.validate_on_submit():
            user = User.query.filter_by(name=self.form.name.data).first()
            if user is None or not user.verify_password(self.form.password.data):
                flash(messages.bad_credentials, category='error')
                return redirect(url_for('.login'))
            login_user(user, self.form.remember_me.data)
            return redirect(request.args.get('next') or url_for('.index'))
        return render_template(self.template, login_form=self.form)


class Logout(BaseView):
    decorators = [login_required]

    def __init__(self):
        BaseView.__init__(self)
        if not validate_csrf(self.request_args.csrfToken.data):
            abort(400)

    def get(self):
        logout_user()
        flash(messages.user_logged_out, 'info')
        return redirect(url_for('.index'))


class NewPost(BaseView):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def __init__(self):
        BaseView.__init__(self)
        self.template = 'new_post.html'
        self.form = PostForm()

    def get(self):
        self.response_data['post_form'] = self.form

    def post(self):
        if self.form.validate_on_submit():
            taglist = [Tag.query.filter_by(name=tag.name).first() or tag \
                        for tag in self.form.tags.data]
            new_post = Post(self.form.title.data, self.form.content.data,
                        self.form.is_public.data, current_user, taglist)

            db.session.add(new_post)
            db.session.commit()

            flash(messages.post_created, 'info')
            return redirect(url_for('.index'))

        flash(messages.post_creation_error, 'error')
        return render_template(self.template, post_form=self.form)


class EditPost(BaseView):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def __init__(self):
        BaseView.__init__(self)
        self.template = 'edit_post.html'

        if not self.request_args.postId.data:
            abort(400)

        self.post_obj = Post.query.get_or_404(self.request_args.postId.data)

        if self.post_obj.user_id != current_user.id and not current_user.is_admin:
            abort(403)

    def get(self):
        post_form = PostForm().from_model(self.post_obj)
        self.response_data['post_form'] = post_form
        self.response_data['post_id'] = self.post_obj.id

    def post(self):
        form = PostForm()
        if form.validate_on_submit():
            self.post_obj.update(form.title.data, form.content.data,
                                 form.is_public.data, form.tags.data)

            db.session.add(self.post_obj)
            db.session.commit()

            flash(messages.post_edited, 'info')
            return redirect(url_for('.index', postId=self.post_obj.id))

        flash(messages.post_editing_error, 'error')
        return render_template(self.template, post_form=form,
                               post_id=self.post_obj.id)


class DeletePost(EditPost):
    methods = ['GET']

    def __init__(self):
        EditPost.__init__(self)
        if not validate_csrf(self.request_args.csrfToken.data):
            abort(400)

    def get(self):
        db.session.delete(self.post_obj)
        db.session.commit()

        flash(messages.post_deleted, 'info')
        return redirect(url_for('.index'))

