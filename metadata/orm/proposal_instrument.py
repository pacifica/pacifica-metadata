#!/usr/bin/python
"""
Proposal instrument relationship
"""
from peewee import ForeignKeyField, IntegerField, Expression, OP, CompositeKey
from metadata.orm.proposals import Proposals
from metadata.orm.instruments import Instruments
from metadata.orm.base import DB, PacificaModel

class ProposalInstrument(PacificaModel):
    """
    Relates proposals and instrument objects.
    """
    instrument = ForeignKeyField(Instruments, related_name='proposals')
    proposal = ForeignKeyField(Proposals, related_name='instruments')
    hours_estimated = IntegerField(default=-1)

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        PeeWee meta class contains the database and the primary key.
        """
        database = DB
        primary_key = CompositeKey('instrument', 'proposal')
    # pylint: enable=too-few-public-methods

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(ProposalInstrument, self).to_hash()
        obj['instrument_id'] = int(self.instrument.instrument_id)
        obj['proposal_id'] = int(self.proposal.proposal_id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash into the object
        """
        super(ProposalInstrument, self).from_hash(obj)
        if 'instrument_id' in obj:
            self.instrument = Instruments.get(Instruments.instrument_id == obj['instrument_id'])
        if 'proposal_id' in obj:
            self.proposal = Proposals.get(Proposals.proposal_id == obj['proposal_id'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(ProposalInstrument, self).where_clause(kwargs)
        if 'instrument_id' in kwargs:
            instrument = Instruments.get(Instruments.instrument_id == kwargs['instrument_id'])
            where_clause &= Expression(ProposalInstrument.instrument, OP.EQ, instrument)
        if 'proposal_id' in kwargs:
            proposal = Proposals.get(Proposals.proposal_id == kwargs['proposal_id'])
            where_clause &= Expression(ProposalInstrument.proposal, OP.EQ, proposal)
        return where_clause
