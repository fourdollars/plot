# -*- coding: utf-8 -*-
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'views/index.html')
        planets = [
                {'name': 'Planet DebianTW', 'url': 'http://planet.debian.org.tw/'},
                {'name': 'GOT 星球', 'url': 'http://planet.gentoo.tw/'},
                {'name': 'Ubuntu正體中文站-星球', 'url': 'http://www.ubuntu-tw.org/modules/planet/'},
                {'name': 'Kaohsiung Linux User Group', 'url': 'http://kalug.linux.org.tw/planet/'},
                {'name': 'Official Python Planet@Taiwan', 'url': 'http://planet.python.org.tw/'},
                ]
        people = [
                {
                    'name': 'FourDollars', # user specify
                    'feed': 'http://fourdollars.blogspot.com/feeds/posts/default', # user specify
                    'title': 'FourDollars Blog', # fetch from feed
                    'url': 'http://fourdollars.blogspot.com', # fetch from feed
                    },
                ]
        categories = [ 'group', 'people', 'software' ]
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
