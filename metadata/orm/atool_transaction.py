#!/usr/bin/python
# -*- coding: utf-8 -*-
"""TransactionKeyValue links Transactions and Keys and Values objects."""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.base import DB
from metadata.orm.utils import index_hash
from metadata.orm.transactions import Transactions
from metadata.orm.analytical_tools import AnalyticalTools
from metadata.rest.orm import CherryPyAPI


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

    transaction = ForeignKeyField(Transactions, related_name='atools')
    analytical_tool = ForeignKeyField(
        AnalyticalTools, related_name='transactions')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('analytical_tool', 'transaction')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(AToolTransaction, AToolTransaction).elastic_mapping_builder(obj)
        obj['transaction_id'] = {'type': 'integer'}
        obj['analytical_tool_id'] = {'type': 'integer'}

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
        if 'analytical_tool_id' in obj:
            self.analytical_tool = AnalyticalTools.get(
                AnalyticalTools.id == obj['analytical_tool_id']
            )
        if 'transaction_id' in obj:
            self.transaction = Transactions.get(
                Transactions.id == obj['transaction_id'])

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(AToolTransaction, self).where_clause(kwargs)
        if 'analytical_tool_id' in kwargs:
            atool = AnalyticalTools.get(
                AnalyticalTools.id == kwargs['analytical_tool_id'])
            where_clause &= Expression(
                AToolTransaction.analytical_tool, OP.EQ, atool)
        if 'transaction_id' in kwargs:
            trans = Transactions.get(
                Transactions.id == kwargs['transaction_id'])
            where_clause &= Expression(
                AToolTransaction.transaction, OP.EQ, trans)
        return where_clause
