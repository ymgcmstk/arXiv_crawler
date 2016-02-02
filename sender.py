#!/usr/bin/env python
# -*- coding:utf-8 -*-

from checker import Paper
from google.appengine.api import mail
from google.appengine.ext import ndb
from main import  Account
from settings import *
import webapp2

class SendEmail(webapp2.RequestHandler):
    def get(self):
        q = ndb.gql("SELECT * FROM Account")
        accounts = []
        for i in q.iter():
            accounts.append(i)
        q = ndb.gql("SELECT * FROM Paper")
        papers = []
        for i in q.iter():
            papers.append(i)
        for account in accounts:
            self.gen_mail(account, papers)
        for paper in papers:
            paper.key.delete()
        self.response.write('success')
    def gen_mail(self, account, papers):
        content = u''
        written_number = []
        if len(papers) == 0:
            return
        paper_count = 0
        for paper in papers:
            if not paper.area in account.areas:
                continue
            if not account.areas[paper.area]:
                continue
            if paper.number in written_number:
                continue
            paper_count += 1
            content += u'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
            content += paper.title

            content += ', ' + paper.first_author + '\n'
            content += u'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
            content += paper.abstract + '\n\n'
            content += paper.authors
            content = content[:-2] + '\n'
            content += 'http://arxiv.org/pdf/' + paper.number + '\n\n'
            written_number.append(paper.number)
        if paper_count == 0:
            return
        elif paper_count == 1:
            content = '1 paper has been uploaded.\n\n' + content
            title = 'arXiv checker (1 paper)'
        else:
            content = '%d papers have been uploaded.\n\n' % paper_count + content
            title = 'arXiv checker (%d papers)' % paper_count
        self.gmail(title, content, account.email)
    def gmail(self, title, content, address):
        mail.send_mail(sender=SENDER_ADDRESS,
                       to=address,
                       subject=title,
                       body=content)

app = webapp2.WSGIApplication([
    ('/crons/sender', SendEmail)
], debug=True)
