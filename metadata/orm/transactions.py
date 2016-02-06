#!/usr/bin/python

from peewee import IntegerField, TextField, CharField, BigIntegerField, ForeignKeyField, BooleanField
from metadata.orm.base import DB, PacificaModel
from metadata.orm.users import Users
from datetime import datetime

class Transactions(PacificaModel):
    transaction_id = BigIntegerField(default=-1, primary_key=True)
    verified = BooleanField(default=False)
    submitter = ForeignKeyField(Users, related_name='transactions')

