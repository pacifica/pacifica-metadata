#!/usr/bin/python

from peewee import IntegerField, TextField, CharField
from metadata.orm import DB, PacificaModel

class ProductContributor(PacificaModel):
    product_id = IntegerField(default=-1)
    author_id = IntegerField(default=-1)
    author_precedence = IntegerField(default=1)

    class Meta(object):
        database = DB
        primary_key = CompositeKey('product_id', 'author_id')

