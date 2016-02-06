#!/usr/bin/python

from peewee import IntegerField, TextField, CharField
from metadata.orm.base import DB, PacificaModel

class Keys(PacificaModel):
    key_id = IntegerField(default=-1)
    key = CharField(default="")

