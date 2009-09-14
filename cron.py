# -*- coding: utf-8 -*-
import os
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from models.data import *

class Cron(webapp.RequestHandler):
    def get(self, action):
        cron = self.request.headers.get('X-AppEngine-Cron')
        #if cron is not None and cron == 'true':
        if action == 'fetch':
            self.fetch()
        elif action == 'mail':
            self.mail()
    def fetch(self):
        feeds = Feed.all().order('created')
        count = feeds.count()
        counter = Counter.get_by_key_name('last_fetch')
        if counter is None:
            counter = Counter(key_name='last_fetch', count=0)
        else:
            counter.count = counter.count + 1
            if counter.count >= count:
                counter.count = 0
        counter.put()
        feed = feeds.fetch(1, offset=counter.count)
        self.response.out.write(feed[0].feed)
    def mail(self):
        pass

application = webapp.WSGIApplication(
                                     [('/cron/(.*)', Cron)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
