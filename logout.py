#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import webapp2
import jinja2
import logging
from google.appengine.api import users

class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_logout_url(self.request.uri))

app = webapp2.WSGIApplication([
    ('/logout/logout', LogoutHandler),
], debug=True)
