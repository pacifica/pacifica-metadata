#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Citation proposal relationship."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.utils import index_hash, unicode_type
from pacifica.metadata.orm.transaction_release import TransactionRelease
from pacifica.metadata.orm.doidatasets import DOIDataSets
from pacifica.metadata.orm.base import DB
from pacifica.metadata.rest.orm import CherryPyAPI


class DOITransaction(CherryPyAPI):
    """
    Relates DOI entries with transaction release entries.

    Attributes:
        +-------------------+--------------------------------------------+
        | Name              | Description                                |
        +===================+============================================+
        | doi               | Link to the DOI model                      |
        +-------------------+--------------------------------------------+
        | transaction       | Link to the TransactionRelease model       |
        +-------------------+--------------------------------------------+
    """

    doi = ForeignKeyField(
        DOIDataSets, related_name='doi_entries', to_field='doi')
    transaction = ForeignKeyField(
        TransactionRelease, to_field='transaction', related_name='doi_releases')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('doi', 'transaction')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(DOITransaction, DOITransaction).elastic_mapping_builder(obj)
        obj['transaction'] = {'type': 'integer'}
        obj['doi'] = \
            {'type': 'text', 'fields': {'keyword': {
                'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(DOITransaction, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(self.__data__['doi']),
                                int(self.__data__['transaction']))
        obj['doi'] = unicode_type(self.__data__['doi'])
        obj['transaction'] = int(self.__data__['transaction'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(DOITransaction, self).from_hash(obj)
        self._set_only_if('doi', obj, 'doi', lambda: DOIDataSets.get(
            DOIDataSets.doi == obj['doi']))
        self._set_only_if('transaction', obj, 'transaction', lambda: TransactionRelease.get(
            TransactionRelease.transaction == obj['transaction']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(DOITransaction, cls).where_clause(kwargs)
        return cls._where_attr_clause(where_clause, kwargs, ['doi', 'transaction'])
