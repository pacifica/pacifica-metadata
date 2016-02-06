#!/usr/bin/python

from peewee import ForeignField, CompositeKey
from metadata.orm.base import DB, PacificaModel
from metadata.orm.files import Files
from metadata.orm.transactions import Transactions

class FileGroup(PacificaModel):
    file_id = ForeignField(Files, related_name='file_id')
    transaction_id = ForeignField(Transactions, related_name='transaction_id')

    class Meta(object):
        database = DB
        primary_key = CompositeKey('file_id', 'transaction_id')

