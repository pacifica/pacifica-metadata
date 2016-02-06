#!/usr/bin/python

from peewee import IntegerField, TextField, CharField
from metadata.orm.base import DB, PacificaModel

class Contributors(PacificaModel):
    author_id = IntegerField(default=-1, primary_key=True)
    first_name = CharField(default="")
    middle_initial = CharField(default="")
    last_name = CharField(default="")
    network_id = CharField(default="")
    dept_code = CharField(default="")
    institution_name = TextField(default="")

