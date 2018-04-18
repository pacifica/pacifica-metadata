#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Contains the model for metadata analytical tools."""
from peewee import CharField, Expression, OP
from metadata.orm.base import DB
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import unicode_type


class Meta:
    database = DB


class DataReleaseStates(CherryPyAPI):
    """
    DataReleaseStates model class for metadata.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | name              | generic state name                  |
        +-------------------+-------------------------------------+
        | display_name      | generic state name for display      |
        +-------------------+-------------------------------------+
        | encoding          | encoding for the name               |
        +-------------------+-------------------------------------+
    """

    name = CharField(default='')
    display_name = CharField(default='')
    encoding = CharField(default='UTF8')

    @classmethod
    def create_table(cls):
        super(DataReleaseStates, DataReleaseStates).create_table(cls)
        names = {
            'not_released': {'index': 0, 'identifier': 'Not Released'},
            'released': {'index': 1, 'identifier': 'Released'},
            'minted': {'index': 2, 'identifier': 'Minted'},
            'published': {'index': 5, 'identifier': 'Published'},
        }
        DataReleaseStates.insert_many([
            {
                'id': names[name]['index'],
                'name': name,
                'display_name': names[name]['identifier']
            } for name in names]).execute()

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(DataReleaseStates, DataReleaseStates).elastic_mapping_builder(obj)
        obj['name'] = obj['encoding'] = \
            {'type': 'text', 'fields': {'keyword': {
                'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(DataReleaseStates, self).to_hash(**flags)
        obj['_id'] = int(self.id)
        obj['name'] = unicode_type(self.name)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(DataReleaseStates, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = obj['_id']
            # pylint: enable=invalid-name
        if 'name' in obj:
            self.name = unicode_type(obj['name'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])

    def where_clause(self, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(DataReleaseStates, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(
                DataReleaseStates.id, OP.EQ, kwargs['_id'])
        if 'name' in kwargs:
            name_oper = OP.EQ
            if 'name_operator' in kwargs:
                name_oper = getattr(OP, kwargs['name_operator'])
            where_clause &= Expression(
                DataReleaseStates.name, name_oper, kwargs['name'])
        if 'encoding' in kwargs:
            where_clause &= Expression(
                DataReleaseStates.encoding, OP.EQ, kwargs['encoding'])
        return where_clause
