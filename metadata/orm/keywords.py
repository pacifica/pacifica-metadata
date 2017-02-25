#!/usr/bin/python
"""Keywords linked to citations."""
from peewee import CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI
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

    keyword = CharField(default='')
    encoding = CharField(default='UTF8')

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(Keywords, Keywords).elastic_mapping_builder(obj)
        obj['keyword'] = obj['encoding'] = {'type': 'string'}

    def to_hash(self):
        """Convert the object to a hash."""
        obj = super(Keywords, self).to_hash()
        obj['_id'] = int(self.id) if self.id is not None else obj['_id']
        obj['keyword'] = unicode_type(self.keyword)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(Keywords, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: int(obj['_id']))
        self._set_only_if('keyword', obj, 'keyword', lambda: unicode_type(obj['keyword']))
        self._set_only_if('encoding', obj, 'encoding', lambda: str(obj['encoding']))

    @staticmethod
    def _where_attr_clause(where_clause, kwargs):
        for key in ['keyword', 'encoding']:
            if key in kwargs:
                key_oper = OP.EQ
                if '{0}_operator'.format(key) in kwargs:
                    key_oper = getattr(OP, kwargs['{0}_operator'.format(key)].upper())
                where_clause &= Expression(getattr(Keywords, key), key_oper, kwargs[key])
        return where_clause

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(Keywords, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Keywords.id, OP.EQ, kwargs['_id'])
        return self._where_attr_clause(where_clause, kwargs)
