#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Citation proposal relationship."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.utils import index_hash, unicode_type
from pacifica.metadata.orm.proposals import Proposals
from pacifica.metadata.orm.citations import Citations
from pacifica.metadata.orm.base import DB
from pacifica.metadata.rest.orm import CherryPyAPI


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

    citation = ForeignKeyField(Citations, backref='proposals')
    proposal = ForeignKeyField(Proposals, backref='citations')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('citation', 'proposal')
    # pylint: enable=too-few-public-methods

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
        self._set_only_if('citation_id', obj, 'citation',
                          lambda: Citations.get(Citations.id == obj['citation_id']))
        self._set_only_if('proposal_id', obj, 'proposal',
                          lambda: Proposals.get(Proposals.id == obj['proposal_id']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(CitationProposal, cls).where_clause(kwargs)
        attrs = ['citation', 'proposal']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
