# -*- coding: utf-8 -*-
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models.data import *

class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'views/index.html')
        categories = Category.all().fetch(1000)
        feeds = Feed.all().fetch(1000)
        planets = Planet.all().fetch(1000)
        vars = {
                'title': 'Planet Linux of Taiwan',
                'categories': categories,
                'feeds': feeds,
                'planets': planets,
                }
        self.response.out.write(template.render(path, vars))

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
