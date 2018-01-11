#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CitationContributor links citations and their authors."""
from peewee import IntegerField, ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.utils import index_hash
from metadata.orm.base import DB
from metadata.orm.citations import Citations
from metadata.orm.contributors import Contributors
from metadata.rest.orm import CherryPyAPI


class CitationContributor(CherryPyAPI):
    """
    CitationsContributors data model.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | citation          | Link to the Citation model          |
        +-------------------+-------------------------------------+
        | author            | Link to the Contributor model       |
        +-------------------+-------------------------------------+
        | author_precedence | Order of the Author in the Citation |
        +-------------------+-------------------------------------+
    """

    citation = ForeignKeyField(Citations, related_name='authors')
    author = ForeignKeyField(Contributors, related_name='citations')
    author_precedence = IntegerField(default=1)

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains database and primary keys."""

        database = DB
        primary_key = CompositeKey('citation', 'author')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(CitationContributor, CitationContributor).elastic_mapping_builder(obj)
        obj['citation_id'] = obj['author_id'] = obj['author_precedence'] = \
            {'type': 'integer'}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(CitationContributor, self).to_hash(**flags)
        obj['_id'] = index_hash(int(self._data['citation']), int(self._data['author']))
        obj['citation_id'] = int(self._data['citation'])
        obj['author_id'] = int(self._data['author'])
        obj['author_precedence'] = int(self.author_precedence)
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(CitationContributor, self).from_hash(obj)
        if 'citation_id' in obj:
            self.citation = Citations.get(Citations.id == obj['citation_id'])
        if 'author_id' in obj:
            self.author = Contributors.get(Contributors.id == obj['author_id'])
        if 'author_precedence' in obj:
            self.author_precedence = int(obj['author_precedence'])

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(CitationContributor, self).where_clause(kwargs)
        if 'citation_id' in kwargs:
            citation = Citations.get(Citations.id == kwargs['citation_id'])
            where_clause &= Expression(
                CitationContributor.citation, OP.EQ, citation)
        if 'author_id' in kwargs:
            author = int(kwargs['author_id'])
            where_clause &= Expression(
                CitationContributor.author, OP.EQ, author)
        if 'author_precedence' in kwargs:
            auth_prec = int(kwargs['author_precedence'])
            where_clause &= Expression(
                CitationContributor.author_precedence, OP.EQ, auth_prec)
        return where_clause
