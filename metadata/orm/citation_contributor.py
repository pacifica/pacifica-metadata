#!/usr/bin/python
"""
CitationContributor links citations and their authors.
"""
from peewee import IntegerField, ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.base import PacificaModel, DB
from metadata.orm.citations import Citations
from metadata.orm.contributors import Contributors

class CitationContributor(PacificaModel):
    """
    CitationsContributors data model
    """
    citation = ForeignKeyField(Citations, related_name='authors')
    author = ForeignKeyField(Contributors, related_name='citations')
    author_precedence = IntegerField(default=1)

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        PeeWee meta class contains database and primary keys.
        """
        database = DB
        primary_key = CompositeKey('citation', 'author')
    # pylint: enable=too-few-public-methods

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(CitationContributor, self).to_hash()
        obj['citation_id'] = int(self.citation.citation_id)
        obj['author_id'] = int(self.author.author_id)
        obj['author_precedence'] = int(self.author_precedence)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash into the object
        """
        super(CitationContributor, self).from_hash(obj)
        if 'citation_id' in obj:
            self.citation = Citations.get(Citations.citation_id == obj['citation_id'])
        if 'author_id' in obj:
            self.author = Contributors.get(Contributors.author_id == obj['author_id'])
        if 'author_precedence' in obj:
            self.author_precedence = int(obj['author_precedence'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(CitationContributor, self).where_clause(kwargs)
        if 'citation_id' in kwargs:
            citation = Citations.get(Citations.citation_id == kwargs['citation_id'])
            where_clause &= Expression(CitationContributor.citation, OP.EQ, citation)
        if 'person_id' in kwargs:
            author = Contributors.get(Contributors.author_id == kwargs['author_id'])
            where_clause &= Expression(CitationContributor.author, OP.EQ, author)
        if 'author_precedence' in kwargs:
            auth_prec = int(kwargs['author_precedence'])
            where_clause &= Expression(CitationContributor.author_precedence, OP.EQ, auth_prec)
        return where_clause
