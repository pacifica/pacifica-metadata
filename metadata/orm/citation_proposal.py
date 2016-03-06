#!/usr/bin/python
"""
Citation proposal relationship
"""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.proposals import Proposals
from metadata.orm.citations import Citations
from metadata.orm.base import DB, PacificaModel

class CitationProposal(PacificaModel):
    """
    Relates citations with proposals
    """
    citation = ForeignKeyField(Citations, related_name='propoasls')
    proposal = ForeignKeyField(Proposals, related_name='citations')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        PeeWee meta class contains the database and the primary key.
        """
        database = DB
        primary_key = CompositeKey('citation', 'proposal')
    # pylint: enable=too-few-public-methods

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(CitationProposal, self).to_hash()
        obj['citation_id'] = int(self.citation.citation_id)
        obj['proposal_id'] = int(self.proposal.proposal_id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash into the object
        """
        super(CitationProposal, self).from_hash(obj)
        if 'citation_id' in obj:
            self.citation = Citations.get(Citations.citation_id == obj['citation_id'])
        if 'proposal_id' in obj:
            self.proposal = Proposals.get(Proposals.proposal_id == obj['proposal_id'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(CitationProposal, self).where_clause(kwargs)
        if 'citation_id' in kwargs:
            citation = Citations.get(Citations.citation_id == kwargs['citation_id'])
            where_clause &= Expression(CitationProposal.citation, OP.EQ, citation)
        if 'proposal_id' in kwargs:
            proposal = Proposals.get(Proposals.proposal_id == kwargs['proposal_id'])
            where_clause &= Expression(CitationProposal.proposal, OP.EQ, proposal)
        return where_clause
