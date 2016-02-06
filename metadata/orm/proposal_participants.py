#!/usr/bin/python

from peewee import IntegerField, TextField, CharField
from metadata.orm import DB, PacificaModel

class ProposalParticipants(PacificaModel):
    proposal_id = CharField(default="")
    person_id = IntegerField(default=-1)
    proposal_author_sw = CharField(default="")
    proposal_co_author_sw = CharField(default="")

    class Meta(object):
        database = DB
        primary_key = CompositeKey('proposal_id', 'person_id')
