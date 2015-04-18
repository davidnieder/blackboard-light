# -*- coding: utf-8 -*-

def date(obj):
    if hasattr(obj, 'strftime'):
        return obj.strftime('%B %d, %Y')
    return obj

def isodate(obj):
    if hasattr(obj, 'date'):
        return obj.date().isoformat()
    return obj

def queryprint(queryargs):
    string = unicode()
    if 'postId' in queryargs:
        string += '%s=%s AND ' %('id', queryargs['postId'])
    if 'user' in queryargs:
        string += '%s=%s AND ' %('user', queryargs['user'])
    if 'tags'in queryargs:
        string += '%s=%s AND ' %('tags', queryargs['tags'])
    if 'sincePost' in queryargs:
        string += '%s=%s AND ' %('since-post', queryargs['sincePost'])
    if 'beforePost' in queryargs:
        string += '%s=%s AND ' %('before-post', queryargs['beforePost'])
    if 'since' in queryargs:
        string += '%s=%s AND ' %('since', queryargs['since'])
    if 'before' in queryargs:
        string += '%s=%s AND ' %('before', queryargs['before'])
    if 'createdOn' in queryargs:
        string += '%s=%s AND ' %('date', queryargs['createdOn'])
    if 'onlyPrivatePosts' in queryargs:
        string += 'only-private-posts AND '
    if 'onlyPublicPosts' in queryargs:
        string += 'only-public-posts AND '
    if 'searchString' in queryargs:
        string += 'contains="%s" AND ' %queryargs['searchString']
    if 'order' in queryargs:
        if queryargs['order'] == 'asc':
            string += '%s=%s AND ' %('order', 'ascending')
        elif queryargs['order'] == 'desc':
            string += '%s=%s AND ' %('order', 'descending')
    return string.rstrip(' AND ')

def init_app(app):
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.filters['date'] = date
    app.jinja_env.filters['isodate'] = isodate
    app.jinja_env.filters['queryprint'] = queryprint
