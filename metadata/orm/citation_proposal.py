#!/usr/bin/python
"""Citation proposal relationship."""
from peewee import ForeignKeyField, CompositeKey, Expression, OP, unicode_type
from metadata.orm.utils import index_hash
from metadata.orm.proposals import Proposals
from metadata.orm.citations import Citations
from metadata.orm.base import DB
from metadata.rest.orm import CherryPyAPI


class CitationProposal(CherryPyAPI):
    """
    Relates citations with proposals.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | citation          | Link to the Citation model          |
        +-------------------+-------------------------------------+
        | proposal          | Link to the Proposal model          |
        +-------------------+-------------------------------------+
    """

    citation = ForeignKeyField(Citations, related_name='propoasls')
    proposal = ForeignKeyField(Proposals, related_name='citations')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('citation', 'proposal')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(CitationProposal, CitationProposal).elastic_mapping_builder(obj)
        obj['citation_id'] = {'type': 'integer'}
        obj['proposal_id'] = {'type': 'text', 'fields': {'keyword': {'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, recursion_depth=1):
        """Convert the object to a hash."""
        obj = super(CitationProposal, self).to_hash(recursion_depth)
        obj['_id'] = index_hash(int(self.citation.id), unicode_type(self.proposal.id))
        obj['citation_id'] = int(self.citation.id)
        obj['proposal_id'] = unicode_type(self.proposal.id)
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(CitationProposal, self).from_hash(obj)
        if 'citation_id' in obj:
            self.citation = Citations.get(Citations.id == obj['citation_id'])
        if 'proposal_id' in obj:
            self.proposal = Proposals.get(Proposals.id == obj['proposal_id'])

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(CitationProposal, self).where_clause(kwargs)
        if 'citation_id' in kwargs:
            citation = Citations.get(Citations.id == kwargs['citation_id'])
            where_clause &= Expression(CitationProposal.citation, OP.EQ, citation)
        if 'proposal_id' in kwargs:
            proposal = Proposals.get(Proposals.id == kwargs['proposal_id'])
            where_clause &= Expression(CitationProposal.proposal, OP.EQ, proposal)
        return where_clause
