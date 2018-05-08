#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Proposal instrument relationship."""
from peewee import ForeignKeyField, CompositeKey
from metadata.orm.utils import index_hash, unicode_type
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
        obj = super(ProposalInstrument, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(
            self.__data__['proposal']), int(self.__data__['instrument']))
        obj['instrument_id'] = int(self.__data__['instrument'])
        obj['proposal_id'] = unicode_type(self.__data__['proposal'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(ProposalInstrument, self).from_hash(obj)
        self._set_only_if(
            'instrument_id', obj, 'instrument',
            lambda: Instruments.get(Instruments.id == obj['instrument_id'])
        )
        self._set_only_if(
            'proposal_id', obj, 'proposal',
            lambda: Proposals.get(Proposals.id == obj['proposal_id'])
        )

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(ProposalInstrument, cls).where_clause(kwargs)
        attrs = ['instrument', 'proposal']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
