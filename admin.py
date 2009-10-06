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
    def get(self, controller=None, action=None, id=None):
        if controller == 'request':
            self.request_controller(action, id)
            self.redirect('/admin')
            return
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
    def post(self, controller=None, action=None, id=None):
        if controller == 'config':
            self.config(action)
        elif controller == 'planet':
            self.planet(action)
        elif controller == 'category':
            self.category(action)
        elif controller == 'feed':
            self.feed(action)
        elif controller == 'request':
            self.request(action)
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
        email = self.request.get('email')
        category = self.request.get('category')
        if name is None or url is None or category is None:
            return
        query = Category.all()
        parent = query.filter('name =', category).get()
        if parent is None:
            return
        feed = Feed(name=name, feed=url, category=parent, email=email)
        feed.put()
        memcache.delete('feeds')
    def request_controller(self, action, id):
        if action == 'apply':
            request = Request.get(id)
            query = Category.all()
            parent = query.filter('name =', request.category).get()
            feed = Feed(name=request.name, feed=request.feed, category=parent, email=request.email, avatar=request.avatar)
            feed.put()
            memcache.delete('feeds')
            request.delete()

application = webapp.WSGIApplication([
    ('/admin', Dashboard),
    ('/admin/(.*)/(.*)/(.*)', Dashboard),
    ('/admin/(.*)/(.*)', Dashboard),
    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
