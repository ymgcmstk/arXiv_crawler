#!/usr/bin/env python
# coding: utf-8

from db_classes import LastPaper, Paper
from google.appengine.ext import ndb
from settings import *
import time
import urllib2
import webapp2

class CrawlArXiv(webapp2.RequestHandler):
    def get(self):
        for area in TARGLIST:
            self.main(area)
        self.response.write('success')
    def gen_recent_url(self, area):
        return "http://arxiv.org/list/" + area + "/recent"
    def get_html(self, url):
        time.sleep(INTERVAL)
        fp = urllib2.urlopen(url)
        html = fp.read()
        fp.close()
        return html
    def getstr_fromto(self, this_str, start, end):
        this_str_start = 0
        temp_len = 0
        for i in start:
            this_str_start = this_str.find(i, this_str_start) + len(i)
            if this_str_start < len(i):
                return ""
        this_str_end = this_str_start
        temp_len = 0
        for i in end:
            this_str_end = this_str.find(i, this_str_end + temp_len)
            temp_len = len(i)
        if this_str_start < 0:
            return ""
        if this_str_end < 0:
            return this_str[this_str_start:]
        return this_str[this_str_start:this_str_end]
    def parse_abs(self, number, area):
        this_html = self.get_html("http://arxiv.org/abs/" + number)
        paper = Paper()
        paper.number = number
        paper.title = self.getstr_fromto(this_html, ['Title:</span>', '\n'], ['</h1>'])
        authors = ''
        temp_str = "Authors:</span>"
        safety_count = 0
        while True:
            temp_str = self.getstr_fromto(this_html[this_html.find('<h1 class="title mathjax">'):this_html.find('<div class="dateline">')], [temp_str, '<a href=', '>'], ['</a>'])
            if len(temp_str) == 0 or safety_count > 20:
                break
            authors += temp_str + ', '
            safety_count += 1
        paper.first_author = authors.split(', ')[0]
        paper.authors = authors
        paper.abstract = self.getstr_fromto(this_html, ['Abstract:</span>'], ['</blockquote>']).replace('\n', ' ')
        updated_at = self.getstr_fromto(this_html, ['last revised '], [' ('])
        if len(updated_at) == 0:
            updated_at = self.getstr_fromto(this_html, ['Submitted on '], [')'])
        paper.updated_at = updated_at
        paper.area = area
        paper.put()
    def parse_recent(self, url):
        num_list = []
        this_html = self.get_html(url)
        this_start = ['"Abstract">arXiv:']
        safety_count = 0
        while True:
            safety_count += 1
            this_num = self.getstr_fromto(this_html, this_start, ["</a>"])
            if this_num == "" or safety_count > PAPER_LIMIT:
                break
            num_list.append(this_num)
            this_start = ['arXiv:' + this_num, '"Abstract">arXiv:']
        return num_list
    def get_info(self, area, end_paper):
        num_list = self.parse_recent(self.gen_recent_url(area))
        this_papers = {}
        total = len(num_list)
        count = 0
        for i in num_list:
            if i == end_paper:
                break
            if count == 0:
                self.update_end_paper(area, i)
            count += 1
            self.parse_abs(i, area)
    def update_end_paper(self, area, number):
        q = ndb.gql("SELECT * FROM LastPaper WHERE area = :1", area)
        end_paper = q.get()
        if end_paper is None:
            end_paper = LastPaper()
            end_paper.area = area
        end_paper.number = number
        end_paper.put()
    def main(self, area):
        end_paper = ndb.gql("SELECT * FROM LastPaper WHERE area = :1", area).get()
        if end_paper is not None:
            end_paper_number = end_paper.number
        else:
            end_paper_number = None
        self.get_info(area, end_paper_number)

app = webapp2.WSGIApplication([
    ('/crons/crawler', CrawlArXiv)
], debug=True)
