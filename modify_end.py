#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import webapp2
import jinja2
import logging
from google.appengine.ext import ndb
from checker import EndPaper
from main import BaseHandler

class ModifyEndHandler(BaseHandler):
    def get(self):
        self.render('modify_end.html')
    def post(self):
        self.horizontal_line('EndPapers')
        q = ndb.gql("SELECT * FROM EndPaper WHERE area = :1", self.request.get('area'))
        end_paper = q.get()
        if end_paper is None:
            self.redirect('/utils/disp')
        end_paper.number = self.request.get('number')
        end_paper.put()
        self.redirect('/utils/disp')

    def horizontal_line(self, name):
        self.response.write('---------------------------<br>')
        self.response.write(name + '<br>')
        self.response.write('---------------------------<br>')

app = webapp2.WSGIApplication([
    ('/utils/modify_end', ModifyEndHandler),
], debug=True)
