#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Keywords linked to citations."""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.base import DB
from metadata.orm.citations import Citations
from metadata.orm.transaction_release import TransactionRelease
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import index_hash, unicode_type


class CitationRelease(CherryPyAPI):
    """
    CitationRelease Model.

    Attributes:
        +-------------------+--------------------------------------------+
        | Name              | Description                                |
        +===================+============================================+
        | release           | Link to the TransactionRelease model       |
        +-------------------+--------------------------------------------+
        | citation          | Link to the Citations model                |
        +-------------------+--------------------------------------------+
    """

    citation = ForeignKeyField(Citations, related_name='release_entries')
    release = ForeignKeyField(TransactionRelease, related_name='citations')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('citation', 'release')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(CitationRelease, CitationRelease).elastic_mapping_builder(obj)
        obj['citation_id'] = obj['release_id'] = {'type': 'integer'}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(CitationRelease, self).to_hash(**flags)
        obj['_id'] = index_hash(
            int(self._data['release']),
            int(self._data['citation'])
        )
        obj['release_id'] = int(self._data['release'])
        obj['citation_id'] = int(self._data['citation'])
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(CitationRelease, self).from_hash(obj)
        if 'citation_id' in obj:
            self.citation = Citations.get(
                Citations.id == obj['citation_id'])
        if 'release_id' in obj:
            self.release = TransactionRelease.get(TransactionRelease.id == obj['release_id'])

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(CitationRelease, self).where_clause(kwargs)
        if 'release_id' in kwargs:
            where_clause &= Expression(
                CitationRelease.release, OP.EQ, int(kwargs['release_id']))
        if 'citation_id' in kwargs:
            where_clause &= Expression(
                CitationRelease.citation, OP.EQ,
                int(kwargs['citation_id'])
            )
        return where_clause
