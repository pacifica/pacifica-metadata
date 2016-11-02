#!/usr/bin/python
"""Keywords linked to citations."""
from peewee import CharField, ForeignKeyField, Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.citations import Citations
from metadata.orm.utils import unicode_type


class Keywords(CherryPyAPI):
    """
    Keywords Model.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | citation          | Link to the Citation model          |
        +-------------------+-------------------------------------+
        | keyword           | keyword in the citation             |
        +-------------------+-------------------------------------+
        | encoding          | encoding of the keyword             |
        +-------------------+-------------------------------------+
    """

    citation = ForeignKeyField(Citations, related_name='keywords')
    keyword = CharField(default='')
    encoding = CharField(default='UTF8')

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(Keywords, Keywords).elastic_mapping_builder(obj)
        obj['citation_id'] = {'type': 'integer'}
        obj['keyword'] = obj['encoding'] = {'type': 'string'}

    def to_hash(self):
        """Convert the object to a hash."""
        obj = super(Keywords, self).to_hash()
        obj['_id'] = int(self.id)
        obj['keyword'] = unicode_type(self.keyword)
        obj['encoding'] = str(self.encoding)
        obj['citation_id'] = int(self.citation.id)
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(Keywords, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = obj['_id']
            # pylint: enable=invalid-name
        if 'keyword' in obj:
            self.keyword = unicode_type(obj['keyword'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])
        if 'citation_id' in obj:
            self.citation = Citations.get(Citations.id == obj['citation_id'])

    @staticmethod
    def _where_attr_clause(where_clause, kwargs):
        for key in ['keyword', 'encoding']:
            if key in kwargs:
                key_oper = OP.EQ
                if '{0}_operator'.format(key) in kwargs:
                    key_oper = getattr(OP, kwargs['{0}_operator'.format(key)])
                where_clause &= Expression(getattr(Keywords, key), key_oper, kwargs[key])
        return where_clause

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(Keywords, self).where_clause(kwargs)
        if 'citation_id' in kwargs:
            citation = Citations.get(Citations.id == kwargs['citation_id'])
            where_clause &= Expression(Keywords.citation, OP.EQ, citation)
        if '_id' in kwargs:
            where_clause &= Expression(Keywords.id, OP.EQ, kwargs['_id'])
        return self._where_attr_clause(where_clause, kwargs)
