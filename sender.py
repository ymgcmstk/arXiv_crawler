# -*- coding:utf-8 -*-

import webapp2
from google.appengine.ext import ndb
from main import TARGLIST, Account
from checker import Paper
from google.appengine.api import mail

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
            self.main(account, papers)
        for paper in papers:
            paper.key.delete()
        self.response.write('success')
    def main(self, account, papers):
        content = u''
        written_number = []
        if len(papers) == 0:
            return
        paper_count = 0
        for paper in papers:
            if not paper.area in account.areas:
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
        if paper_count == 1:
            content = '1 paper has been uploaded.\n\n' + content
            title = 'MIL-arXiv (1 paper)'
        else:
            content = '%d papers have been uploaded.\n\n' % paper_count + content
            title = 'MIL-arXiv (%d papers)' % paper_count
        self.gmail(title, content, account.email)
    def gmail(self, title, content, address):
        mail.send_mail(sender="papers@mil-arxiv.appspotmail.com",
                       to=address,
                       subject=title,
                       body=content)

app = webapp2.WSGIApplication([('/crons/sender', SendEmail)])
