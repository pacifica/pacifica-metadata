#!/usr/bin/python

from peewee import IntegerField, TextField, CharField, BigIntegerField, DateTimeField, BooleanField
from metadata.orm.base import DB, PacificaModel
from datetime import datetime

class Transactions(PacificaModel):
    transaction_id = BigIntegerField(default=-1, primary_key=True)
    verified = BooleanField(default=False)
    person_id = IntegerField(default=-1)
