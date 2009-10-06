#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from google.appengine.api import memcache,images,mail
from google.appengine.ext import webapp
from google.appengine.ext.db import BadValueError
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models.data import *
from recaptcha.client import captcha

class MainPage(webapp.RequestHandler):
    def get(self, *arg):
        categories = Category.getList()
        feeds = Feed.getList()
        planets = Planet.getList()
        config = Config.getData()
        vars = {
                'title': config.name,
                'categories': categories,
                'feeds': feeds,
                'planets': planets,
                }
        path = os.path.join(os.path.dirname(__file__), 'views/index.html')
        self.response.out.write(template.render(path, vars))

class Join(webapp.RequestHandler):
    def get(self):
        categories = Category.getList()
        feeds = Feed.getList()
        planets = Planet.getList()
        config = Config.getData()
        if config and self.request.host != 'localhost:8080':
            chtml = captcha.displayhtml(
                    public_key = config.public_key,
                    use_ssl = False,
                    error = None)
        else:
            chtml = ''
        vars = {
                'title': 'Join - %s' % (config.name),
                'categories': categories,
                'feeds': feeds,
                'planets': planets,
                'captchahtml': chtml,
                }
        path = os.path.join(os.path.dirname(__file__), 'views/join.html')
        self.response.out.write(template.render(path, vars))
    def post(self):
        challenge = self.request.get('recaptcha_challenge_field')
        response  = self.request.get('recaptcha_response_field')
        remoteip  = os.environ.get('REMOTE_ADDR')
        config = Config.getData()
        if self.request.host == 'localhost:8080':
            name = self.request.get('name')
            feed = self.request.get('feed')
            data = self.request.get('avatar')
            email = self.request.get('email')
            category = self.request.get('category')
            image = images.Image(data)
            image.im_feeling_lucky()
            if image.width > 100 or image.height > 100:
                image.resize(width=100, height=100)
            avatar = Avatar(data=image.execute_transforms(output_encoding=images.PNG))
            avatar.put()
            join = Request(
                    name=name,
                    feed=feed,
                    email=email,
                    remoteip=remoteip,
                    category=category,
                    valid=True,
                    avatar=avatar)
            join.put()
            self.redirect('/join')
            return
        cResponse = captcha.submit(
                challenge,
                response,
                config.private_key,
                remoteip)
        if cResponse.is_valid:
            try:
                name = self.request.get('name')
                feed = self.request.get('feed')
                data = self.request.get('avatar')
                email = self.request.get('email')
                category = self.request.get('category')
                image = images.Image(data)
                image.im_feeling_lucky()
                if image.width > 100 or image.height > 100:
                    image.resize(width=100, height=100)
                avatar = Avatar(data=image.execute_transforms(output_encoding=images.PNG))
                avatar.put()
                join = Request(
                        name=name,
                        feed=feed,
                        email=email,
                        remoteip=remoteip,
                        category=category,
                        avatar=avatar)
                join.put()
                categories = Category.getList()
                feeds = Feed.getList()
                planets = Planet.getList()
                config = Config.getData()
                vars = {
                        'title': 'Join - %s' % (config.name),
                        'categories': categories,
                        'feeds': feeds,
                        'planets': planets,
                        'message': 'Done! Please check your email.',
                        }
                mail.send_mail(
                        email,
                        email,
                        'Request Validate of %s' % (config.name),
                        'Hi %s,\n Please visit http://%s/validate/%s' % (name, self.request.host, join.key())
                        )
                path = os.path.join(os.path.dirname(__file__), 'views/result.html')
                self.response.out.write(template.render(path, vars))
            except BadValueError:
                self.redirect('/join')
        else:
            self.redirect('/join')

class AvatarController(webapp.RequestHandler):
    def get(self, key):
        avatar = Avatar.get(key)
        if avatar is not None:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(avatar.data)

class Validate(webapp.RequestHandler):
    def get(self, key_name):
        request = Request.get(key_name)
        if request and request.valid == False:
            request.valid = True
            request.put()
            categories = Category.getList()
            feeds = Feed.getList()
            planets = Planet.getList()
            config = Config.getData()
            vars = {
                    'title': 'Join - %s' % (config.name),
                    'categories': categories,
                    'feeds': feeds,
                    'planets': planets,
                    'message': 'Your email has be validated. Please wait for the review of admin.',
                    }
            path = os.path.join(os.path.dirname(__file__), 'views/result.html')
            self.response.out.write(template.render(path, vars))
        else:
            self.redirect('/')

application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/join', Join),
    ('/category/(.*)', MainPage),
    ('/avatar/(.*)', AvatarController),
    ('/validate/(.*)', Validate),
    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
