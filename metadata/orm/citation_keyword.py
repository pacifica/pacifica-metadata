#!/usr/bin/python
"""Keywords linked to citations."""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.utils import index_hash
from metadata.orm.citations import Citations
from metadata.orm.keywords import Keywords
from metadata.orm.base import DB
from metadata.rest.orm import CherryPyAPI


class CitationKeyword(CherryPyAPI):
    """
    CitationKeywords Model.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | citation          | Link to the Citation model          |
        +-------------------+-------------------------------------+
        | keyword           | Link to the Keyword model           |
        +-------------------+-------------------------------------+
    """

    citation = ForeignKeyField(Citations, related_name='keywords')
    keyword = ForeignKeyField(Keywords, related_name='citations')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('citation', 'keyword')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(CitationKeyword, CitationKeyword).elastic_mapping_builder(obj)
        obj['citation_id'] = {'type': 'integer'}
        obj['keyword_id'] = {'type': 'integer'}

    def to_hash(self, flags):
        """Convert the object to a hash."""
        obj = super(CitationKeyword, self).to_hash(flags)
        # pylint: disable=no-member
        obj['_id'] = index_hash(int(self.citation.id), int(self.keyword.id))
        obj['citation_id'] = int(self.citation.id)
        obj['keyword_id'] = int(self.keyword.id)
        # pylint: enable=no-member
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(CitationKeyword, self).from_hash(obj)
        self._set_only_if('citation_id', obj, 'citation', lambda: Citations.get(Citations.id == obj['citation_id']))
        self._set_only_if('keyword_id', obj, 'keyword', lambda: Keywords.get(Keywords.id == obj['keyword_id']))

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(CitationKeyword, self).where_clause(kwargs)
        if 'citation_id' in kwargs:
            citation = Citations.get(Citations.id == kwargs['citation_id'])
            where_clause &= Expression(CitationKeyword.citation, OP.EQ, citation)
        if 'keyword_id' in kwargs:
            keyword = Keywords.get(Keywords.id == kwargs['keyword_id'])
            where_clause &= Expression(CitationKeyword.keyword, OP.EQ, keyword)
        return where_clause
