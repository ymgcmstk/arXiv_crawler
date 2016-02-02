#!/usr/bin/env python
# -*- coding: utf-8 -*-

APP_NAME = 'arXiv crawler'
TARGLIST = ['cs.CV', 'cs.CL', 'cs.NE', 'stat.ML']
SENDER_ADDRESS = 'papers@XXXXXXXXX.appspotmail.com'

def filter_user(user, obj):
    if user is None:
        obj.redirect(users.create_login_url(obj.request.uri))
        return True
    if not '@XXXXXXXXX' in user.email():
        obj.response.write('Access denied.')
        obj.response.write('<br>')
        obj.response.write('<a href="' + users.create_logout_url(obj.request.uri) + '">Logout</a>')
        return True
    return False
