#!/usr/bin/python

from peewee import IntegerField, TextField, CharField, FloatField
from metadata.orm import DB, PacificaModel

class Journals(PacificaModel):
    journal_id = IntegerField(default=-1, primary_key=True)
    journal_name = CharField(default="")
    impact_factor = FloatField(default=-1.0)
    website_url = CharField(default="")

