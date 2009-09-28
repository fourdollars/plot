# -*- coding: utf-8 -*-
from google.appengine.ext import db

class Category(db.Model):
    name = db.StringProperty(required=True)

class Counter(db.Model):
    count = db.IntegerProperty(required=True)

class Feed(db.Model):
    name = db.StringProperty(required=True)
    feed = db.LinkProperty(required=True)
    title = db.StringProperty(default=None)
    url = db.LinkProperty(default=None)
    category = db.ReferenceProperty(Category, collection_name='feeds', required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class Planet(db.Model):
    name = db.StringProperty(required=True)
    url = db.LinkProperty(required=True)

class JoinRequest(db.Model):
    name = db.StringProperty(required=True)
    feed = db.LinkProperty(required=True)
    avatar = db.BlobProperty()
