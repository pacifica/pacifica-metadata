#!/usr/bin/python

from peewee import IntegerField, TextField, CharField
from metadata.orm.base import DB, PacificaModel

class Values(PacificaModel):
    value_id = IntegerField(default=-1, primary_key=True)
    value = CharField(default="")

