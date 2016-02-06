#!/usr/bin/python

from peewee import ForeignKeyField, CharField, BigIntegerField, DateTimeField, BooleanField
from metadata.orm.base import DB, PacificaModel
from metadata.orm.transactions import Transactions
from datetime import datetime

class Files(PacificaModel):
    file_id = BigIntegerField(default=-1, primary_key=True)
    name = CharField(default="")
    subdir = CharField(default="")
    vtime = DateTimeField(default=datetime.now)
    verified = BooleanField(default=False)
    size = BigIntegerField(default=-1)
    transaction = ForeignKeyField(Transactions, related_name='files')
