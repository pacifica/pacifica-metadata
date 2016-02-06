#!/usr/bin/python

from peewee import IntegerField, TextField, CharField
from metadata.orm import DB, PacificaModel

class InstitutionPerson(PacificaModel):
    person_id = IntegerField(default=-1, primary_key=True)
    institution_id = IntegerField(default=-1)

