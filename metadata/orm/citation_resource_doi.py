#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Keywords linked to citations."""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.base import DB
from metadata.orm.citations import Citations
from metadata.orm.doidatasets import DOIDataSets
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import index_hash, unicode_type


class CitationResourceDOI(CherryPyAPI):
    """
    CitationResourceDOI Model.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | doi               | Link to the DOIDataSets model       |
        +-------------------+-------------------------------------+
        | citation          | Link to the Citations model         |
        +-------------------+-------------------------------------+
    """

    citation = ForeignKeyField(Citations, related_name='doi')
    doi = ForeignKeyField(
        DOIDataSets, related_name='resources', to_field='doi')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('citation', 'doi')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(CitationResourceDOI, CitationResourceDOI).elastic_mapping_builder(obj)
        obj['doi'] = {'type': 'text', 'fields': {'keyword': {
            'type': 'keyword', 'ignore_above': 256}}}
        obj['citation_id'] = {'type': 'integer'}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(CitationResourceDOI, self).to_hash(**flags)
        obj['_id'] = index_hash(
            unicode_type(self.__data__['doi']),
            int(self.__data__['citation'])
        )
        obj['doi'] = unicode_type(self.doi.doi)
        obj['citation_id'] = int(self.__data__['citation'])
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(CitationResourceDOI, self).from_hash(obj)
        if 'citation_id' in obj:
            self.citation = Citations.get(
                Citations.id == obj['citation_id'])
        if 'doi' in obj:
            self.doi = DOIDataSets.get(DOIDataSets.doi == obj['doi'])

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(CitationResourceDOI, self).where_clause(kwargs)
        if 'doi' in kwargs:
            where_clause &= Expression(
                CitationResourceDOI.doi, OP.EQ, unicode_type(kwargs['doi']))
        if 'citation_id' in kwargs:
            where_clause &= Expression(
                CitationResourceDOI.citation, OP.EQ,
                int(kwargs['citation_id'])
            )
        return where_clause
