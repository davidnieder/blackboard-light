# -*- coding: utf-8 -*-

from . import blog
import views


# index
blog.add_url_rule('/', view_func=views.Index.as_view('index'))

# login, logout
blog.add_url_rule('/login', view_func=views.Login.as_view('login'))
blog.add_url_rule('/logout', view_func=views.Logout.as_view('logout'))

# new/edit post
blog.add_url_rule('/newPost', view_func=views.NewPost.as_view('new_post'))
blog.add_url_rule('/editPost', view_func=views.EditPost.as_view('edit_post'))
blog.add_url_rule('/deletePost', view_func=views.DeletePost.as_view('delete_post'))

# search
blog.add_url_rule('/search', view_func=views.Search.as_view('search'))
