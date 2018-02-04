#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Keywords linked to citations."""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.base import DB
from metadata.orm.transactions import Transactions
from metadata.orm.doidatasets import DOIDataSets
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import index_hash, unicode_type


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
    doi = ForeignKeyField(DOIDataSets, related_name='resources')

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
            unicode_type(self._data['doi']),
            int(self._data['transaction'])
        )
        obj['doi'] = unicode_type(self.doi.doi)
        obj['transaction_id'] = int(self._data['transaction'])
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(DOIResource, self).from_hash(obj)
        if 'transaction_id' in obj:
            self.transaction = Transactions.get(
                Transactions.id == obj['transaction_id'])
        if 'doi' in obj:
            self.doi = DOIDataSets.get(DOIDataSets.doi == obj['doi'])

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(DOIResource, self).where_clause(kwargs)
        if 'doi' in kwargs:
            where_clause &= Expression(
                DOIResource.doi, OP.EQ,
                DOIDataSets.get(DOIDataSets.doi == kwargs['doi']).id
            )
        if 'transaction_id' in kwargs:
            where_clause &= Expression(
                DOIResource.transaction, OP.EQ,
                int(kwargs['transaction_id'])
            )
        return where_clause
