# -*- coding: utf-8 -*-
import os
from google.appengine.api import memcache, images
from google.appengine.ext import webapp
from google.appengine.ext.db import BadValueError
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models.data import *
from recaptcha.client import captcha

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

class Join(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'views/join.html')
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
        chtml = captcha.displayhtml(
                public_key = "PUBLIC_KEY",
                use_ssl = False,
                error = None)
        vars = {
                'title': 'Join - Planet Linux of Taiwan',
                'categories': categories,
                'feeds': feeds,
                'planets': planets,
                'captchahtml': chtml,
                }
        self.response.out.write(template.render(path, vars))
    def post(self):
        challenge = self.request.get('recaptcha_challenge_field')
        response  = self.request.get('recaptcha_response_field')
        remoteip  = os.environ.get('REMOTE_ADDR')
        cResponse = captcha.submit(
                challenge,
                response,
                "PRIVATE_KEY",
                remoteip)

        if cResponse.is_valid:
            try:
                name = self.request.get('name')
                feed = self.request.get('feed')
                avatar = self.request.get('avatar')
                image = images.Image(avatar)
                image.im_feeling_lucky()
                if image.width > 100 or image.height > 100:
                    image.resize(width=100, height=100)
                join = JoinRequest(name=name, feed=feed, avatar=image.execute_transforms(output_encoding=images.PNG))
                join.put()
                path = os.path.join(os.path.dirname(__file__), 'views/result.html')
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
                        'title': 'Join - Planet Linux of Taiwan',
                        'categories': categories,
                        'feeds': feeds,
                        'planets': planets,
                        'message': 'Done!',
                        }
                self.response.out.write(template.render(path, vars))
            except BadValueError:
                self.redirect('/join')
        else:
            error = cResponse.error_code
            self.redirect('/join')

class Avatar(webapp.RequestHandler):
    def get(self, key_name):
        request = JoinRequest.get(key_name)
        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(request.avatar)

application = webapp.WSGIApplication(
                                     [
                                         ('/', MainPage),
                                         ('/join', Join),
                                         ('/category/(.*)', MainPage),
                                         ('/avatar/(.*)', Avatar),
                                         ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
