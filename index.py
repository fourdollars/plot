# -*- coding: utf-8 -*-
import os
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models.data import *

class MainPage(webapp.RequestHandler):
    def get(self, *arg):
        path = os.path.join(os.path.dirname(__file__), 'views/index.html')
        categories = memcache.get('categories')
        if categories is None:
            categories = Category.all().fetch(1000)
            memcache.set(key='categories', value=categories, time=3600)
        feeds = memcache.get('feeds')
        if feeds is None:
            feeds = Feed.all().fetch(1000)
            memcache.set(key='feeds', value=feeds, time=3600)
        planets = memcache.get('planets')
        if planets is None:
            planets = Planet.all().fetch(1000)
            memcache.set(key='planets', value=planets, time=3600)
        vars = {
                'title': 'Planet Linux of Taiwan',
                'categories': categories,
                'feeds': feeds,
                'planets': planets,
                }
        self.response.out.write(template.render(path, vars))

application = webapp.WSGIApplication(
                                     [
                                         ('/', MainPage),
                                         ('/join', MainPage),
                                         ('/category/(.*)', MainPage),
                                         ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
