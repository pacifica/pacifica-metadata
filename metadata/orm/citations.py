#!/usr/bin/python

from peewee import Model, Meta, IntegerField, TextField
from peewee import CharField, DateTimeField
from metadata.orm import DB
from datetime.datetime import now

class Citations(Model):
    product_id = IntegerField(default=-1, primary_key=True)
    article_title = TextField(default="")
    journal_id = IntegerField(default=-1)
    journal_volume = IntegerField(default=-1)
    journal_issue = IntegerField(default=-1)
    page_range = CharField(default="")
    abstract_text = TextField(default="")
    xml_text = TextField(default="")
    pnnl_clearance_id = CharField(default="")
    doi_reference = CharField(default="")
    last_change_date = DateTimeField(default=now)
    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)
    deleted = DateTimeField(default=now)

    class Meta(object):
        database = DB
