#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import users

APP_NAME       = 'arXiv crawler'
INTERVAL       = 5
PAPER_LIMIT    = 20
SENDER_ADDRESS = 'papers@XXXXXXXXX.appspotmail.com'
TARGLIST       = ['cs.CV', 'cs.CL', 'cs.NE', 'stat.ML']

def filter_user(user, obj):
    if user is None:
        obj.redirect(users.create_login_url(obj.request.uri))
        return True
    return False
