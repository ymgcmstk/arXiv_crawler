# coding: utf-8

import webapp2
from google.appengine.ext import ndb
from main import TARGLIST, Account
from checker import Paper
from google.appengine.api import mail

class SendEmail:
    def get(self):
        q = ndb.gql("SELECT * FROM Account")
        accounts = q.get()
        q = ndb.gql("SELECT * FROM Paper")
        papers = q.get()
        for account in accounts:
            self.main(account, papers)
        for paper in papers:
            paper.delete()
    def main(self, account, papers, address):
        #どのareaが対象なのかを取得する
        title = 'Today\'s arXiv papers'
        content = ''
        if len(papers) == 0:
            return
        elif len(papers) == 1:
            content += '1 paper have been uploaded today.\n\n'
        else:
            content += '%d papers have been uploaded today.\n\n' % len(papers)
        for paper in papers:
            if not paper.area in account.areas:
                continue
            content += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
            content += paper.title + ', ' + paper.first_author + '\n'
            #content += paper.title + '\n'
            content += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
            content += paper.abstract + '\n\n'
            content += paper.authors
            content = content[:-2] + '\n'
            content += 'http://arxiv.org/pdf/' + paper.number + '\n\n'
        gmail(title, content, account.email)
    def gmail(self, title, content, address):
        mail.send_mail(sender="yamaguchi@mi.t.u-tokyo.ac.jp",
                       to=address,
                       subject=title,
                       body=content)

app = webapp2.WSGIApplication([('/crons/sender', SendEmail)])
