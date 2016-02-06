#!/usr/bin/python

from peewee import Model, Meta, IntegerField, TextField
from peewee import CharField, DateTimeField
from metadata.orm import DB
from datetime.datetime import now

class Contributors(Model):
    author_id = IntegerField(default=-1, primary_key=True)
    first_name = CharField(default="")
    middle_initial = CharField(default="")
    last_name = CharField(default="")
    network_id = CharField(default="")
    dept_code = CharField(default="")
    institution_name = TextField(default="")
    last_change_date = DateTimeField(default=now)
    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)
    deleted = DateTimeField(default=now)

    class Meta(object):
        database = DB
