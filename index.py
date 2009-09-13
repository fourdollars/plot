# -*- coding: utf-8 -*-
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models.data import *

class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'views/index.html')
        planets = Planet.all()
        people = People.all()
        categories = Category.all()
        vars = {
                'title': 'Planet Linux of Taiwan',
                'planets': planets,
                'categories': categories,
                'people': people,
                }
        self.response.out.write(template.render(path, vars))

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
