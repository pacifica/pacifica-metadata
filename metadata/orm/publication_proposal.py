#!/usr/bin/python

from peewee import IntegerField, TextField, CharField, CompositeKey
from metadata.orm.base import DB, PacificaModel

class PublicationProposal(PacificaModel):
    citation_id = IntegerField(default=-1)
    proposal_id = IntegerField(default=-1)

    class Meta(object):
        database = DB
        primary_key = CompositeKey('citation_id', 'proposal_id')
