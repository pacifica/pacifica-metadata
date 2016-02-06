#!/usr/bin/python

from peewee import Model, Meta, IntegerField, TextField
from peewee import CharField, DateTimeField
from metadata.orm import DB
from datetime.datetime import now

class Keywords(Model):
    keyword_id = IntegerField(default=-1, primary_key=True)
    product_id = IntegerField(default=-1)
    keyword = CharField(default="")
    last_change_date = DateTimeField(default=now)
    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)
    deleted = DateTimeField(default=now)

    class Meta(object):
        database = DB

