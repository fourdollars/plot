# -*- coding: utf-8 -*-
import os
from google.appengine.ext import webapp
from google.appengine.ext.db import BadValueError
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models.data import *

class Dashboard(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'views/admin.html')
        planets = Planet.all()
        people = People.all()
        categories = Category.all()
        vars = {
                'title': 'Dashboard - <a href="/">Planet Linux of Taiwan</a>',
                'planets': planets,
                'categories': categories,
                'people': people,
                }
        self.response.out.write(template.render(path, vars))
    def post(self):
        try:
            type = self.request.get('type')
            action = self.request.get('action')
            if type == None or action == None:
                self.redirect('/admin')
            if type == 'planet':
                name = self.request.get('name')
                url = self.request.get('url')
                if name == None or url == None:
                    self.redirect('/admin')
                planet = Planet(name=name, url=url)
                planet.put()
            elif type == 'category':
                name = self.request.get('name')
                if name == None:
                    self.redirect('/admin')
                category = Category(name=name)
                category.put()
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
