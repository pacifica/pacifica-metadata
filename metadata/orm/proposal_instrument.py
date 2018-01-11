#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Proposal instrument relationship."""
from peewee import ForeignKeyField, Expression, OP, CompositeKey, unicode_type
from metadata.orm.utils import index_hash
from metadata.orm.proposals import Proposals
from metadata.orm.instruments import Instruments
from metadata.orm.base import DB
from metadata.rest.orm import CherryPyAPI


class ProposalInstrument(CherryPyAPI):
    """
    Relates proposals and instrument objects.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | instrument        | Link to the Instrument model        |
        +-------------------+-------------------------------------+
        | proposal          | Link to the Proposal model          |
        +-------------------+-------------------------------------+
    """

    instrument = ForeignKeyField(Instruments, related_name='proposals')
    proposal = ForeignKeyField(Proposals, related_name='instruments')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('instrument', 'proposal')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(ProposalInstrument, ProposalInstrument).elastic_mapping_builder(obj)
        obj['instrument_id'] = {'type': 'integer'}
        obj['proposal_id'] = {'type': 'text', 'fields': {
            'keyword': {'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        fast = flags.get('fast', False)
        obj = super(ProposalInstrument, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(
            self._data['proposal']), int(self._data['instrument']))
        obj['instrument_id'] = int(self._data['instrument'])
        obj['proposal_id'] = unicode_type(self._data['proposal'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(ProposalInstrument, self).from_hash(obj)
        if 'instrument_id' in obj:
            self.instrument = Instruments.get(
                Instruments.id == obj['instrument_id'])
        if 'proposal_id' in obj:
            self.proposal = Proposals.get(Proposals.id == obj['proposal_id'])

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(ProposalInstrument, self).where_clause(kwargs)
        if 'instrument_id' in kwargs:
            instrument = int(kwargs['instrument_id'])
            where_clause &= Expression(
                ProposalInstrument.instrument, OP.EQ, instrument)
        if 'proposal_id' in kwargs:
            proposal = kwargs['proposal_id']
            where_clause &= Expression(
                ProposalInstrument.proposal, OP.EQ, proposal)
        return where_clause
