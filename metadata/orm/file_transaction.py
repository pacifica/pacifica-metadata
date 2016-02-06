#!/usr/bin/python

from peewee import IntegerField, TextField, CharField, CompositeKey
from metadata.orm.base import DB, PacificaModel

class FileGroup(PacificaModel):
    file_id = IntegerField(default=-1)
    transaction_id = IntegerField(default=-1)

    class Meta(object):
        database = DB
        primary_key = CompositeKey('file_id', 'transaction_id')

