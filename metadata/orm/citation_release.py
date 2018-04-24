#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Keywords linked to citations."""
from peewee import ForeignKeyField, CompositeKey
from metadata.orm.base import DB
from metadata.orm.citations import Citations
from metadata.orm.transaction_release import TransactionRelease
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import index_hash


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
        obj['citation'] = obj['release'] = {'type': 'integer'}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(CitationRelease, self).to_hash(**flags)
        obj['_id'] = index_hash(
            int(self.__data__['release']),
            int(self.__data__['citation'])
        )
        obj['release'] = int(self.__data__['release'])
        obj['citation'] = int(self.__data__['citation'])
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(CitationRelease, self).from_hash(obj)
        self._set_only_if('citation', obj, 'citation', lambda: Citations.get(
            Citations.id == obj['citation']))
        self._set_only_if('release', obj, 'release', lambda: TransactionRelease.get(
            TransactionRelease.id == obj['release']))

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(CitationRelease, self).where_clause(kwargs)
        return self._where_attr_clause(where_clause, kwargs, ['citation', 'release'])
