# -*- coding: utf-8 -*-
import os
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.db import BadValueError
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models.data import *

class Dashboard(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'views/admin.html')
        categories = Category.all().fetch(1000)
        memcache.set(key='categories', value=categories, time=3600)
        feeds = Feed.all().fetch(1000)
        memcache.set(key='feeds', value=feeds, time=3600)
        planets = Planet.all().fetch(1000)
        memcache.set(key='planets', value=planets, time=3600)
        vars = {
                'title': 'Dashboard - Planet Linux of Taiwan',
                'categories': categories,
                'feeds': feeds,
                'planets': planets,
                }
        self.response.out.write(template.render(path, vars))
    def post(self):
        try:
            type = self.request.get('type')
            action = self.request.get('action')
            if type is None or action is None:
                self.redirect('/admin')
            if type == 'planet':
                name = self.request.get('name')
                url = self.request.get('url')
                if name is None or url is None:
                    self.redirect('/admin')
                planet = Planet(name=name, url=url)
                planet.put()
            elif type == 'category':
                name = self.request.get('name')
                if name is None:
                    self.redirect('/admin')
                category = Category(name=name)
                category.put()
            elif type == 'feed':
                name = self.request.get('name')
                url = self.request.get('url')
                category = self.request.get('category')
                if name is None or url is None or category is None:
                    self.redirect('/admin')
                query = Category.all()
                parent = query.filter('name =', category).get()
                if parent is None:
                    self.redirect('/admin')
                feed = Feed(name=name, feed=url, category=parent)
                feed.put()
            self.redirect('/admin')
        except BadValueError:
            self.redirect('/admin')

application = webapp.WSGIApplication(
                                     [('/admin', Dashboard)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
