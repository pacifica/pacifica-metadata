#!/usr/bin/python

from peewee import IntegerField, TextField, CharField, DateField
from metadata.orm.base import DB, PacificaModel
from datetime import datetime

class Proposals(PacificaModel):
    proposal_id = CharField(default="", primary_key=True)
    title = TextField(default="")
    abstract = TextField(default="")
    science_theme = CharField(default="")
    science_theme_id = IntegerField(default=-1)
    proposal_type = CharField(default="")
    submitted_date = DateField(default=datetime.now)
    accepted_date = DateField(default=datetime.now)
    actual_start_date = DateField(default=datetime.now)
    actual_end_date = DateField(default=datetime.now)
