#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import webapp2
import jinja2
import logging
from google.appengine.api import users

class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user() is not None:
            self.redirect(users.create_logout_url(self.request.uri))
        #self.redirect('/')

app = webapp2.WSGIApplication([
    ('/utils/logout', LogoutHandler),
])
