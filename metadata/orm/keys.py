#!/usr/bin/python
"""Contains the model for metadata keys."""
from peewee import CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import unicode_type


class Keys(CherryPyAPI):
    """
    Keys model class for metadata.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | key               | generic metadata key                |
        +-------------------+-------------------------------------+
        | encoding          | encoding for the key                |
        +-------------------+-------------------------------------+
    """

    key = CharField(default='', index=True)
    encoding = CharField(default='UTF8')

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(Keys, Keys).elastic_mapping_builder(obj)
        obj['key'] = obj['encoding'] = {'type': 'string'}

    def to_hash(self):
        """Convert the object to a hash."""
        obj = super(Keys, self).to_hash()
        obj['_id'] = int(self.id)
        obj['key'] = unicode_type(self.key)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(Keys, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = obj['_id']
            # pylint: enable=invalid-name
        if 'key' in obj:
            self.key = unicode_type(obj['key'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])

    def where_clause(self, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(Keys, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Keys.id, OP.EQ, kwargs['_id'])
        for key in ['key', 'encoding']:
            if key in kwargs:
                key_oper = OP.EQ
                if '{0}_operator'.format(key) in kwargs:
                    key_oper = getattr(OP, kwargs['{0}_operator'.format(key)].upper())
                where_clause &= Expression(getattr(Keys, key), key_oper, kwargs[key])
        return where_clause
