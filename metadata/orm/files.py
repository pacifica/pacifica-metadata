#!/usr/bin/python

from peewee import IntegerField, TextField, CharField, BigIntegerField, DateTimeField, BooleanField
from metadata.orm.base import DB, PacificaModel
from datetime import datetime

class Files(PacificaModel):
    file_id = BigIntegerField(default=-1, primary_key=True)
    name = CharField(default="")
    subdir = CharField(default="")
    transaction_id = BigIntegerField(default=-1)
    vtime = DateTimeField(default=datetime.now)
    verified = BooleanField(default=False)
    size = BigIntegerField(default=-1)
