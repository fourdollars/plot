#! /usr/bin/env python
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
        categories = Category.getList()
        feeds = Feed.getList()
        planets = Planet.getList()
        config = Config.getData()
        requests = Request.all().fetch(1000)
        vars = {
                'title': 'Dashboard - %s' % (config.name),
                'categories': categories,
                'feeds': feeds,
                'planets': planets,
                'requests': requests,
                'config': config,
                }
        path = os.path.join(os.path.dirname(__file__), 'views/admin.html')
        self.response.out.write(template.render(path, vars))
    def post(self, action, id):
        if id == 'config':
            self.config(action)
        elif id == 'planet':
            self.planet(action)
        elif id == 'category':
            self.category(action)
        elif id == 'feed':
            self.feed(action)
        self.redirect('/admin')
    def config(self, action):
        name = self.request.get('name')
        public_key = self.request.get('public_key')
        private_key = self.request.get('private_key')
        config = Config.getData()
        config.name = name
        config.public_key = public_key
        config.private_key = private_key
        config.put()
        memcache.delete('config')
    def planet(self, action):
        name = self.request.get('name')
        url = self.request.get('url')
        if name is None or url is None:
            return
        planet = Planet(name=name, url=url)
        planet.put()
        memcache.delete('planets')
    def category(self, action):
        name = self.request.get('name')
        if name is None:
            return
        category = Category(name=name)
        category.put()
        memcache.delete('categories')
    def feed(self, action):
        name = self.request.get('name')
        url = self.request.get('url')
        category = self.request.get('category')
        if name is None or url is None or category is None:
            return
        query = Category.all()
        parent = query.filter('name =', category).get()
        if parent is None:
            return
        feed = Feed(name=name, feed=url, category=parent)
        feed.put()
        memcache.delete('feeds')

application = webapp.WSGIApplication([
    ('/admin', Dashboard),
    ('/admin/(.*)/(.*)', Dashboard),
    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
