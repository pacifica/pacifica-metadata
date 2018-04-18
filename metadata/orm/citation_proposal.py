#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Citation proposal relationship."""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.utils import index_hash, unicode_type
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

    citation = ForeignKeyField(Citations, related_name='proposals')
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
        obj['proposal_id'] = {'type': 'text', 'fields': {
            'keyword': {'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(CitationProposal, self).to_hash(**flags)
        obj['_id'] = index_hash(int(self.__data__['citation']),
                                unicode_type(self.__data__['proposal']))
        obj['citation_id'] = int(self.__data__['citation'])
        obj['proposal_id'] = unicode_type(self.__data__['proposal'])
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
            citation = int(kwargs['citation_id'])
            where_clause &= Expression(
                CitationProposal.citation, OP.EQ, citation)
        if 'proposal_id' in kwargs:
            proposal = kwargs['proposal_id']
            where_clause &= Expression(
                CitationProposal.proposal, OP.EQ, proposal)
        return where_clause
