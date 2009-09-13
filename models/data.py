# -*- coding: utf-8 -*-
from google.appengine.ext import db

class Category(db.Model):
    name = db.StringProperty(required=True)

class People(db.Model):
    name = db.StringProperty(required=True)
    feed = db.LinkProperty(required=True)
    title = db.StringProperty(default=None)
    url = db.LinkProperty(default=None)
    category = db.ReferenceProperty(Category, collection_name='people', required=True)

class Planet(db.Model):
    name = db.StringProperty(required=True)
    url = db.LinkProperty(required=True)
