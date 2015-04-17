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
        string += '%s=%s AND ' %('Id', queryargs['postId'])
    if 'user' in queryargs:
        string += '%s=%s AND ' %('User', queryargs['user'])
    if 'tags'in queryargs:
        string += '%s=%s AND ' %('Tags', queryargs['tags'])
    if 'sincePost' in queryargs:
        string += '%s=%s AND ' %('Since-Post', queryargs['sincePost'])
    if 'beforePost' in queryargs:
        string += '%s=%s AND ' %('Before-Post', queryargs['beforePost'])
    if 'since' in queryargs:
        string += '%s=%s AND ' %('Since', queryargs['since'])
    if 'before' in queryargs:
        string += '%s=%s AND ' %('Before', queryargs['before'])
    if 'createdOn' in queryargs:
        string += '%s=%s AND ' %('Date', queryargs['createdOn'])
    if 'onlyPrivatePosts' in queryargs:
        string += 'Only-Private-Posts AND '
    if 'onlyPublicPosts' in queryargs:
        string += 'Only-Public-Posts AND '
    if 'order' in queryargs:
        string += '%s=%s AND ' %('Order', queryargs['order'])
    return string.rstrip(' AND ')

def init_app(app):
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.filters['date'] = date
    app.jinja_env.filters['isodate'] = isodate
    app.jinja_env.filters['queryprint'] = queryprint
