# -*- coding: utf-8 -*-

from . import api
from . import views


# post query endpoint
api.add_url_rule('/posts', view_func=views.Posts.as_view('posts'))

# post modifiers
api.add_url_rule('/posts', view_func=views.DeletePost.as_view('delete_post'))
