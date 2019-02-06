#!/usr/bin/python
# -*- coding: utf-8 -*-
"""TransactionKeyValue links Transactions and Keys and Values objects."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.base import DB
from pacifica.metadata.orm.utils import index_hash, unicode_type
from pacifica.metadata.orm.proposals import Proposals
from pacifica.metadata.orm.analytical_tools import AnalyticalTools
from pacifica.metadata.rest.orm import CherryPyAPI


class AToolProposal(CherryPyAPI):
    """
    TransactionKeyValue attributes are foreign keys.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | proposal          | Link to the Proposals model         |
        +-------------------+-------------------------------------+
        | analytical_tool   | Link to the AnalyticalTools model   |
        +-------------------+-------------------------------------+
    """

    proposal = ForeignKeyField(Proposals, backref='atools')
    analytical_tool = ForeignKeyField(AnalyticalTools, backref='proposals')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('analytical_tool', 'proposal')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(AToolProposal, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(self.__data__['proposal']),
                                int(self.__data__['analytical_tool']))
        obj['proposal_id'] = unicode_type(self.__data__['proposal'])
        obj['analytical_tool_id'] = int(self.__data__['analytical_tool'])

        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(AToolProposal, self).from_hash(obj)
        self._set_only_if('proposal_id', obj, 'proposal',
                          lambda: Proposals.get(Proposals.id == obj['proposal_id']))
        self._set_only_if('analytical_tool_id', obj, 'analytical_tool',
                          lambda: AnalyticalTools.get(
                              AnalyticalTools.id == obj['analytical_tool_id']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(AToolProposal, cls).where_clause(kwargs)
        attrs = ['proposal', 'analytical_tool']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
