#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Citation proposal relationship."""
from peewee import ForeignKeyField, CompositeKey
from metadata.orm.utils import index_hash, unicode_type
from metadata.orm.transaction_release import TransactionRelease
from metadata.orm.doidatasets import DOIDataSets
from metadata.orm.base import DB
from metadata.rest.orm import CherryPyAPI


class DOIRelease(CherryPyAPI):
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
    transaction = ForeignKeyField(TransactionRelease, to_field='transaction', related_name='doi_releases')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('doi', 'release')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(DOIRelease, DOIRelease).elastic_mapping_builder(obj)
        obj['release'] = {'type': 'integer'}
        obj['doi'] = \
            {'type': 'text', 'fields': {'keyword': {
                'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(DOIRelease, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(self.__data__['doi']),
                                int(self.__data__['release']))
        obj['doi'] = unicode_type(self.__data__['doi'])
        obj['release'] = int(self.__data__['release'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(DOIRelease, self).from_hash(obj)
        self._set_only_if('doi', obj, 'doi', lambda: DOIDataSets.get(
            DOIDataSets.doi == obj['doi']))
        self._set_only_if('release', obj, 'release', lambda: TransactionRelease.get(
            TransactionRelease.id == obj['release']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(DOIRelease, cls).where_clause(kwargs)
        return cls._where_attr_clause(where_clause, kwargs, ['doi', 'release'])
