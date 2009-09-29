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
        requests = JoinRequest.all().fetch(1000)
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
    def post(self):
        type = self.request.get('type')
        action = self.request.get('action')
        if type is None and action is None:
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
        elif type == 'config':
            name = self.request.get('name')
            public_key = self.request.get('public_key')
            private_key = self.request.get('private_key')
            config = Config.getData()
            config.name = name
            config.public_key = public_key
            config.private_key = private_key
            config.put()
            memcache.set(key='config', value=config, time=3600)
        self.redirect('/admin')

application = webapp.WSGIApplication(
                                     [('/admin', Dashboard)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
