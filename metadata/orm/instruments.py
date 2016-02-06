#!/usr/bin/python

from peewee import IntegerField, TextField, CharField
from metadata.orm import DB, PacificaModel

class Instruments(PacificaModel):
    instrument_id = IntegerField(default=-1)
    display_name = CharField(default="")
    instrument_name = CharField(default="")
    name_short = CharField(default="")

