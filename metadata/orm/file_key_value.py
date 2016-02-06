#!/usr/bin/python

from peewee import ForeignKeyField, CompositeKey
from metadata.orm.base import DB, PacificaModel
from metadata.orm.files import Files
from metadata.orm.values import Values
from metadata.orm.keys import Keys

class FileKeyValue(PacificaModel):
    file = ForeignKeyField(Files, related_name='metadata')
    key = ForeignKeyField(Keys, related_name='metadata')
    value = ForeignKeyField(Values, related_name='metadata')

    class Meta(object):
        database = DB
        primary_key = CompositeKey('file', 'key', 'value')

