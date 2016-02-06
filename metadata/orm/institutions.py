#!/usr/bin/python

from peewee import IntegerField, TextField, CharField
from metadata.orm import DB, PacificaModel

class Institutions(PacificaModel):
    institution_id = IntegerField(default=-1)
    institution_name = TextField(default="")
    association_cd = CharField(default="UNK")
    is_foreign = IntegerField(default=0)

