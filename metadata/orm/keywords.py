#!/usr/bin/python
"""
Keywords linked to citations
"""
from peewee import CharField, ForeignKeyField, Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.citations import Citations

class Keywords(CherryPyAPI):
    """
    Keywords Model
    """
    citation = ForeignKeyField(Citations, related_name='keywords')
    keyword = CharField(default="")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Keywords, Keywords).elastic_mapping_builder(obj)
        obj['citation_id'] = {'type': 'integer'}
        obj['keyword'] = {'type': 'string'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Keywords, self).to_hash()
        obj['_id'] = int(self.id)
        obj['keyword'] = str(self.keyword)
        obj['citation_id'] = int(self.citation.id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash to the object
        """
        super(Keywords, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = obj['_id']
            # pylint: enable=invalid-name
        if 'keyword' in obj:
            self.keyword = obj['keyword']
        if 'citation_id' in obj:
            self.citation = Citations.get(Citations.id == obj['citation_id'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(Keywords, self).where_clause(kwargs)
        if 'citation_id' in kwargs:
            citation = Citations.get(Citations.id == kwargs['citation_id'])
            where_clause &= Expression(Keywords.citation, OP.EQ, citation)
        if '_id' in kwargs:
            where_clause &= Expression(Keywords.id, OP.EQ, kwargs['_id'])
        if 'keyword' in kwargs:
            where_clause &= Expression(Keywords.keyword, OP.EQ, kwargs['keyword'])
        return where_clause
