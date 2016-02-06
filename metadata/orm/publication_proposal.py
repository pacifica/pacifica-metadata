#!/usr/bin/python

from peewee import IntegerField, TextField, CharField
from metadata.orm import DB, PacificaModel

class PublicationProposal(PacificaModel):
    product_id = IntegerField(default=-1)
    proposal_id = IntegerField(default=-1)

    class Meta(object):
        database = DB
        primary_key = CompositeKey('product_id', 'proposal_id')
