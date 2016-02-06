#!/usr/bin/python

from peewee import IntegerField, TextField, CharField
from metadata.orm import DB, PacificaModel

class ProposalInstrument(PacificaModel):
    instrument_id = IntegerField(default=-1)
    proposal_id = IntegerField(default=-1)
    hours_estimated = IntegerField(default=-1)

    class Meta(object)
        database = DB
        primary_key = CompositeKey('instrument_id', 'proposal_id')
