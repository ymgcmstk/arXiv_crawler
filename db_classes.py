#!/usr/bin/env python
# -*- coding:utf-8 -*-

from google.appengine.ext import ndb
import json

class ExtendedJsonProperty(ndb.BlobProperty):
    def _to_base_type(self, value):
        return json.dumps(value)
    def _from_base_type(self, value):
        return json.loads(value)

class Account(ndb.Model):
    uid = ndb.StringProperty()
    email = ndb.TextProperty()
    areas = ExtendedJsonProperty()

class Paper(ndb.Model):
    number = ndb.StringProperty()
    title = ndb.TextProperty()
    first_author = ndb.TextProperty()
    authors = ndb.TextProperty()
    abstract = ndb.TextProperty()
    area = ndb.StringProperty()
    updated_at = ndb.TextProperty()

class LastPaper(ndb.Model):
    number = ndb.TextProperty()
    area = ndb.StringProperty()
