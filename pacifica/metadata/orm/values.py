#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Contains the model for metadata values."""
from peewee import CharField, Expression, OP
from pacifica.metadata.rest.orm import CherryPyAPI
from pacifica.metadata.orm.utils import unicode_type


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

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(Values, self).to_hash(**flags)
        obj['_id'] = int(self.id)
        obj['value'] = unicode_type(self.value)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(Values, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: obj['_id'])
        self._set_only_if('value', obj, 'value',
                          lambda: unicode_type(obj['value']))
        self._set_only_if('encoding', obj, 'encoding',
                          lambda: str(obj['encoding']))

    @classmethod
    def where_clause(cls, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(Values, cls).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Values.id, OP.EQ, kwargs['_id'])
        return cls._where_attr_clause(where_clause, kwargs, ['value', 'encoding'])
