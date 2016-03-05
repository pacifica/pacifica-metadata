#!/usr/bin/python
"""
Keywords linked to citations
"""
from peewee import IntegerField, CharField, ForeignKeyField, Expression, OP
from metadata.orm.base import PacificaModel
from metadata.orm.citations import Citations

class Keywords(PacificaModel):
    """
    Keywords Model
    """
    keyword_id = IntegerField(default=-1, primary_key=True)
    citation = ForeignKeyField(Citations, related_name='keywords')
    keyword = CharField(default="")

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Keywords, self).to_hash()
        obj['keyword_id'] = int(self.keyword_id)
        obj['keyword'] = str(self.keyword)
        obj['citation_id'] = int(self.citation.citation_id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash to the object
        """
        super(Keywords, self).from_hash(obj)
        if 'keyword_id' in obj:
            self.keyword_id = obj['keyword_id']
        if 'keyword' in obj:
            self.keyword = obj['keyword']
        if 'citation_id' in obj:
            self.citation = Citations.get(Citations.citation_id == obj['citation_id'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(Keywords, self).where_clause(kwargs)
        if 'citation_id' in kwargs:
            where_clause &= Expression(Keywords.citation, OP.EQ, Citations.get(Citations.citation_id == kwargs['citation_id']))
        for key in ['keyword_id', 'keyword']:
            if key in kwargs:
                where_clause &= Expression(Keywords.__dict__[key].field, OP.EQ, kwargs[key])
        return where_clause
