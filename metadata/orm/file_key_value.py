#!/usr/bin/python

from peewee import ForeignKeyField, CompositeKey
from metadata.orm.base import DB, PacificaModel
from metadata.orm.files import Files
from metadata.orm.values import Keys
from metadata.orm.keys import Values

class FileKeyValue(PacificaModel):
    file_id = ForeignKeyField(Files, related_name='file_id')
    key_id = ForeignKeyField(Keys, related_name='key_id')
    value_id = ForeignKeyField(Values, related_name='value_id')

    class Meta(object):
        database = DB
        primary_key = CompositeKey('file_id', 'key_id', 'value_id')

