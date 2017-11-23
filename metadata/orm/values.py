#!/usr/bin/python
"""Contains the model for metadata values."""
from peewee import CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import unicode_type


class Values(CherryPyAPI):
    """
    Values model class for metadata.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | value             | generic value for some metadata     |
        +-------------------+-------------------------------------+
        | encoding          | language encoding of the value      |
        +-------------------+-------------------------------------+
    """

    value = CharField(default='', index=True)
    encoding = CharField(default='UTF8')

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(Values, Values).elastic_mapping_builder(obj)
        obj['value'] = obj['encoding'] = \
            {'type': 'text', 'fields': {'keyword': {'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, flags={}):
        """Convert the object to a hash."""
        obj = super(Values, self).to_hash(flags)
        obj['_id'] = int(self.id)
        obj['value'] = unicode_type(self.value)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(Values, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = obj['_id']
            # pylint: enable=invalid-name
        if 'value' in obj:
            self.value = unicode_type(obj['value'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])

    def where_clause(self, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(Values, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Values.id, OP.EQ, kwargs['_id'])
        for key in ['value', 'encoding']:
            if key in kwargs:
                key_oper = OP.EQ
                if '{0}_operator'.format(key) in kwargs:
                    key_oper = getattr(OP, kwargs['{0}_operator'.format(key)].upper())
                where_clause &= Expression(getattr(Values, key), key_oper, kwargs[key])
        return where_clause
