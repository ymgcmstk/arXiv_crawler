#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db_classes import Account
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import ndb
import jinja2
import logging
import os
from settings import *
import webapp2

_EXPIRES_IN = 1

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def make_targ(targlist):
    ret = {}
    for i in targlist:
        ret[i] = False
    return ret

class BaseHandler(webapp2.RequestHandler):
    def render(self, html, values={}):
        template = JINJA_ENVIRONMENT.get_template(html)
        self.response.write(template.render(values))
        return template

class MainHandler(BaseHandler):
    SUCCESS_STR = 'success'
    def get(self):
        user = users.get_current_user()
        if filter_user(user, self):
            return
        q = ndb.gql("SELECT * FROM Account WHERE uid = :1", user.user_id())
        account = q.get()
        if not account:
            account = Account()
            account.uid = user.user_id()
            account.email = user.email()
            account.areas = make_targ(TARGLIST)
            account.put()
        for i in make_targ(TARGLIST):
            if not i in account.areas:
                account.areas[i] = False
        for i in account.areas:
            flg = memcache.get(i)
            if flg is not None:
                account.areas[i] = flg
        success_or_not = False
        if self.SUCCESS_STR in self.request.GET:
            success_or_not = True
        self.render('index.html', {'account': account,
                                   'appname': APP_NAME,
                                   'name': user.nickname().split('@')[0],
                                   'success': success_or_not})

    def post(self):
        user = users.get_current_user()
        q = ndb.gql("SELECT * FROM Account WHERE uid = :1", user.user_id())
        account = q.get()
        account.uid = user.user_id()
        account.email = user.email()
        account.areas = make_targ(TARGLIST)
        for i in self.request.POST:
            account.areas[i] = True
        account.put()
        for i, j in account.areas.items():
            memcache.add(i, j, _EXPIRES_IN)
        self.redirect('/?%s' % self.SUCCESS_STR)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
])
