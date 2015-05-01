#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import webapp2
import jinja2
import logging
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import memcache

_EXPIRES_IN = 1

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

TARGLIST = ['cs.CV', 'cs.CL', 'cs.NE', 'stat.ML']

def make_targ(targlist):
    ret = {}
    for i in targlist:
        ret[i] = False
    return ret

class ExtendedJsonProperty(ndb.BlobProperty):
  def _to_base_type(self, value):
    return json.dumps(value)
  def _from_base_type(self, value):
    return json.loads(value)

class Account(ndb.Model):
    uid = ndb.StringProperty()
    email = ndb.TextProperty()
    areas = ExtendedJsonProperty()

class BaseHandler(webapp2.RequestHandler):
    def render(self, html, values={}):
        template = JINJA_ENVIRONMENT.get_template(html)
        self.response.write(template.render(values))
        return template

class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            self.redirect(users.create_login_url(self.request.uri))
            return
        if not '@mi.t.u-tokyo.ac.jp' in user.email():
            self.response.write('Not Permitted.')
            return
        q = ndb.gql("SELECT * FROM Account WHERE uid = :1", user.user_id())
        account = q.get()
        if not account:
            account = Account()
            account.uid = user.user_id()
            account.email = user.email()
            account.areas = make_targ(TARGLIST)
            account.put()
        for i in account.areas:
            flg = memcache.get(i)
            if flg is not None:
                account.areas[i] = flg
        self.render('index.html', {'account':account,
                                   'name':user.nickname()})

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
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
