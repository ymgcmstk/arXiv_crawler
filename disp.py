#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import webapp2
import jinja2
import logging
from google.appengine.ext import ndb
from main import TARGLIST, Account
from checker import Paper, EndPaper

class DispHandler(webapp2.RequestHandler):
    def get(self):
        self.horizontal_line('Accounts')
        q = ndb.gql("SELECT * FROM Account")
        for i in q.iter():
            self.response.write(i)
            self.response.write('<br>')
        self.horizontal_line('Papers')
        q = ndb.gql("SELECT * FROM Paper")
        for i in q.iter():
            self.response.write(i)
            self.response.write('<br>')
        self.horizontal_line('EndPapers')
        q = ndb.gql("SELECT * FROM EndPaper")
        for i in q.iter():
            self.response.write(i)
            self.response.write('<br>')

    def horizontal_line(self, name):
        self.response.write('---------------------------<br>')
        self.response.write(name + '<br>')
        self.response.write('---------------------------<br>')

app = webapp2.WSGIApplication([
    ('/api/disp', DispHandler),
], debug=True)
