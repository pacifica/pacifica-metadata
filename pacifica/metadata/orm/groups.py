#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Contains model for groups."""
from peewee import CharField, BooleanField, Expression, OP
from pacifica.metadata.rest.orm import CherryPyAPI
from pacifica.metadata.orm.utils import unicode_type


class Groups(CherryPyAPI):
    """
    Groups model and associated fields.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | name              | name of the group                   |
        +-------------------+-------------------------------------+
        | is_admin          | does the group has admin abilities  |
        +-------------------+-------------------------------------+
        | encoding          | encoding for the group name         |
        +-------------------+-------------------------------------+
    """

    name = CharField(default='')
    is_admin = BooleanField(default=False)
    encoding = CharField(default='UTF8')

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(Groups, self).to_hash(**flags)
        obj['_id'] = int(self.id)
        obj['name'] = unicode_type(self.name)
        obj['encoding'] = str(self.encoding)
        obj['is_admin'] = bool(self.is_admin)
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(Groups, self).from_hash(obj)
        # pylint: disable=invalid-name
        if '_id' in obj:
            self.id = int(obj['_id'])
        # pylint: enable=invalid-name
        if 'name' in obj:
            self.name = unicode_type(obj['name'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])
        if 'is_admin' in obj:
            self.is_admin = self._bool_translate(obj['is_admin'])

    @classmethod
    def where_clause(cls, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(Groups, cls).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Groups.id, OP.EQ, kwargs['_id'])
        if 'is_admin' in kwargs:
            kwargs['is_admin'] = cls._bool_translate(kwargs['is_admin'])
        return cls._where_attr_clause(
            where_clause,
            kwargs,
            ['name', 'is_admin', 'encoding']
        )
