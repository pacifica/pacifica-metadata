#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Contains the model for metadata keys."""
from peewee import CharField, Expression, OP
from pacifica.metadata.rest.orm import CherryPyAPI
from pacifica.metadata.orm.utils import unicode_type


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

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(Keys, self).to_hash(**flags)
        obj['_id'] = int(self.id)
        obj['key'] = unicode_type(self.key)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(Keys, self).from_hash(obj)
        self._set_only_if(
            '_id', obj, 'id', lambda: obj['_id']
        )
        self._set_only_if(
            'key', obj, 'key', lambda: unicode_type(obj['key'])
        )
        self._set_only_if(
            'encoding', obj, 'encoding', lambda: str(obj['encoding'])
        )

    @classmethod
    def where_clause(cls, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(Keys, cls).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Keys.id, OP.EQ, kwargs['_id'])
        return cls._where_attr_clause(where_clause, kwargs, ['key', 'encoding'])
