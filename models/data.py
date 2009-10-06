#! /usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.api import memcache
from google.appengine.ext import db

class Counter(db.Model):
    count = db.IntegerProperty(required=True)

class Category(db.Model):
    name = db.StringProperty(required=True)
    @classmethod
    def getList(cls):
        categories = memcache.get('categories')
        if categories is None:
            categories = Category.all().fetch(1000)
            if categories is not None:
                memcache.set(key='categories', value=categories, time=60)
        return categories

class Feed(db.Model):
    name = db.StringProperty(required=True)
    feed = db.LinkProperty(required=True)
    title = db.StringProperty(default=None)
    url = db.LinkProperty(default=None)
    category = db.ReferenceProperty(Category, collection_name='feeds', required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    @classmethod
    def getList(cls):
        feeds = memcache.get('feeds')
        if feeds is None:
            feeds = Feed.all().fetch(1000)
            if feeds is not None:
                memcache.set(key='feeds', value=feeds, time=60)
        return feeds

class Planet(db.Model):
    name = db.StringProperty(required=True)
    url = db.LinkProperty(required=True)
    @classmethod
    def getList(cls):
        planets = memcache.get('planets')
        if planets is None:
            planets = Planet.all().fetch(1000)
            if planets is not None:
                memcache.set(key='planets', value=planets, time=60)
        return planets

class Request(db.Model):
    name = db.StringProperty(required=True)
    feed = db.LinkProperty(required=True)
    avatar = db.BlobProperty()
    email = db.EmailProperty(required=True)
    remoteip = db.StringProperty(required=True)
    valid = db.BooleanProperty(default=False)

class Config(db.Model):
    url = db.LinkProperty()
    name = db.StringProperty()
    public_key = db.StringProperty()
    private_key = db.StringProperty()
    @classmethod
    def getData(cls):
        config = memcache.get('config')
        if config is None:
            config = cls.get_by_key_name('config')
            if config is None:
                config = Config(
                        name = 'Demo Site',
                        key_name = 'config',
                        )
            config.put()
            memcache.set(key='config', value=config, time=60)
        return config
