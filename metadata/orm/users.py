#!/usr/bin/python

from peewee import IntegerField, TextField, CharField
from metadata.orm import DB, PacificaModel

class Users(PacificaModel):
    person_id = IntegerField(default=-1)
    first_name = CharField(default="")
    last_name = CharField(default="")
    network_id = CharField(default="")

