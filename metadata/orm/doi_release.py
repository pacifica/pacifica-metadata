#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Citation proposal relationship."""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
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
        | release           | Link to the TransactionRelease model       |
        +-------------------+--------------------------------------------+
    """

    doi = ForeignKeyField(
        DOIDataSets, related_name='releases', to_field='doi')
    release = ForeignKeyField(TransactionRelease, related_name='doi_entries')

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
        obj['release_id'] = {'type': 'integer'}
        obj['doi_reference'] = \
            {'type': 'text', 'fields': {'keyword': {
                'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(DOIRelease, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(self._data['doi']),
                                int(self._data['release']))
        obj['doi_reference'] = unicode_type(self._data['doi'])
        obj['release_id'] = int(self._data['release'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(DOIRelease, self).from_hash(obj)
        if 'doi_reference' in obj:
            self.doi = DOIDataSets.get(DOIDataSets.doi == obj['doi_reference'])
        if 'release_id' in obj:
            self.release = TransactionRelease.get(
                TransactionRelease.id == obj['release_id'])

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(DOIRelease, self).where_clause(kwargs)
        if 'doi_reference' in kwargs:
            doi = unicode_type(kwargs['doi_reference'])
            where_clause &= Expression(
                DOIRelease.doi, OP.EQ, doi)
        if 'release_id' in kwargs:
            release = kwargs['release_id']
            where_clause &= Expression(
                DOIRelease.release, OP.EQ, release)
        return where_clause
