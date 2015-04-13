# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms.widgets import TextInput
from wtforms.validators import Required, Length, Optional, NumberRange, Regexp, AnyOf
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField, IntegerField, Field, DateField

from .models import Tag


class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(tag.name for tag in self.data)
        else:
            return u''

    def query_string(self):
        return self._value().replace(' ', '')

    def process_formdata(self, valuelist):
        self.data = []
        if valuelist and valuelist[0].replace(' ', ''):
            for x in valuelist[0].split(','):
                tag = Tag(x.strip())
                if tag not in self.data:
                    self.data.append(tag)


class LoginForm(Form):
    name = StringField('Username:', validators=[Required(), Length(3, 40)])
    password = PasswordField('Password:', validators=[Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class PostForm(Form):
    title = StringField('Title:', validators=[Optional(), Length(1,120)])
    content = TextAreaField('Content:', validators=[Required()])
    is_public = BooleanField('Public post', false_values=('false', 'n', ''))
    tags = TagListField('Tags (comma separated):')
    submit = SubmitField('Submit')

    def from_model(self, post):
        self.title.data = post.title
        self.content.data = post.content
        self.is_public.data = post.is_public
        self.tags.data = post.tags
        return self


class RequestArgs(Form):
    postId = IntegerField(validators=[Optional(), NumberRange(min=1)])
    sincePost = IntegerField(validators=[Optional(), NumberRange(min=1)])
    beforePost = IntegerField(validators=[Optional(), NumberRange(min=1)])
    onlyPrivatePosts = BooleanField(default=False)
    onlyPublicPosts = BooleanField(default=False)
    page = IntegerField(validators=[Optional(), NumberRange(min=1)], default=1)
    order = StringField(validators=[Optional(), AnyOf(['desc','asc'])])
    user = StringField()
    tags = TagListField()
    since = DateField()
    before = DateField()
    createdOn = DateField()
    limit = IntegerField(validators=[Optional(), NumberRange(min=1,max=10)],
                         default=5)
    csrfToken = StringField()

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(RequestArgs, self).__init__(csrf_enabled=csrf_enabled,
                                          *args, **kwargs)

