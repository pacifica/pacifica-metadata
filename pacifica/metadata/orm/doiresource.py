#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Keywords linked to citations."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.base import DB
from pacifica.metadata.orm.transactions import Transactions
from pacifica.metadata.orm.doidatasets import DOIDataSets
from pacifica.metadata.rest.orm import CherryPyAPI
from pacifica.metadata.orm.utils import index_hash, unicode_type


class DOIResource(CherryPyAPI):
    """
    Keywords Model.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | doi               | Link to the DOIDataSets model       |
        +-------------------+-------------------------------------+
        | transaction       | Link to the Transactions model      |
        +-------------------+-------------------------------------+
    """

    transaction = ForeignKeyField(Transactions, related_name='doi')
    doi = ForeignKeyField(
        DOIDataSets, related_name='resources', to_field='doi')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('transaction', 'doi')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(DOIResource, DOIResource).elastic_mapping_builder(obj)
        obj['doi'] = {'type': 'text', 'fields': {'keyword': {
            'type': 'keyword', 'ignore_above': 256}}}
        obj['transaction'] = {'type': 'integer'}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(DOIResource, self).to_hash(**flags)
        obj['_id'] = index_hash(
            unicode_type(self.__data__['doi']),
            int(self.__data__['transaction'])
        )
        obj['doi'] = unicode_type(self.__data__['doi'])
        obj['transaction_id'] = int(self.__data__['transaction'])
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(DOIResource, self).from_hash(obj)
        self._set_only_if('transaction_id', obj, 'transaction',
                          lambda: Transactions.get(Transactions.id == obj['transaction_id']))
        self._set_only_if('doi', obj, 'doi',
                          lambda: DOIDataSets.get(DOIDataSets.doi == obj['doi']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(DOIResource, cls).where_clause(kwargs)
        if 'transaction_id' in kwargs:
            kwargs['transaction'] = kwargs.pop('transaction_id')
        return cls._where_attr_clause(where_clause, kwargs, ['doi', 'transaction'])
