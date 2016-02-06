#!/usr/bin/python

from peewee import IntegerField, TextField, CharField, DateField
from metadata.orm import DB, PacificaModel
from datetime.datetime import now

class Proposals(PacificaModel):
    proposal_id = CharField(default="", primary_key=True)
    title = TextField(default="")
    abstract = TextField(default="")
    science_theme = CharField(default="")
    science_theme_id = IntegerField(default=-1)
    proposal_type = CharField(default="")
    submitted_date = DateField(default=now)
    accepted_date = DateField(default=now)
    actual_start_date = DateField(default=now)
    actual_end_date = DateField(default=now)
