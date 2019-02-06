#!/usr/bin/python
# -*- coding: utf-8 -*-
"""TransactionKeyValue links Transactions and Keys and Values objects."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.base import DB
from pacifica.metadata.orm.utils import index_hash
from pacifica.metadata.orm.transactions import Transactions
from pacifica.metadata.orm.analytical_tools import AnalyticalTools
from pacifica.metadata.rest.orm import CherryPyAPI


class AToolTransaction(CherryPyAPI):
    """
    TransactionKeyValue attributes are foreign keys.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | transaction       | Link to the Transactions model      |
        +-------------------+-------------------------------------+
        | analytical_tool   | Link to the AnalyticalTools model   |
        +-------------------+-------------------------------------+
    """

    transaction = ForeignKeyField(Transactions, backref='atools')
    analytical_tool = ForeignKeyField(AnalyticalTools, backref='transactions')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('analytical_tool', 'transaction')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(AToolTransaction, self).to_hash(**flags)
        obj['_id'] = index_hash(int(self.__data__['transaction']),
                                int(self.__data__['analytical_tool']))
        obj['transaction_id'] = int(self.__data__['transaction'])
        obj['analytical_tool_id'] = int(self.__data__['analytical_tool'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(AToolTransaction, self).from_hash(obj)
        self._set_only_if('analytical_tool_id', obj, 'analytical_tool',
                          lambda: AnalyticalTools.get(
                              AnalyticalTools.id == obj['analytical_tool_id']))
        self._set_only_if('transaction_id', obj, 'transaction',
                          lambda: Transactions.get(Transactions.id == obj['transaction_id']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(AToolTransaction, cls).where_clause(kwargs)
        attrs = ['analytical_tool', 'transaction']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
