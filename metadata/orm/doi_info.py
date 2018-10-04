#!/usr/bin/python
# -*- coding: utf-8 -*-
"""DOIInfo stores return info from the minting service about the DOI entry."""
from peewee import ForeignKeyField, CharField, CompositeKey
from metadata.orm.base import DB
from metadata.orm.doi_entries import DOIEntries
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import unicode_type


class DOIInfo(CherryPyAPI):
    """
    DOI Info keys and values for return info from minting service.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | doi               | Link to the DOIEntries model        |
        +-------------------+-------------------------------------+
        | key               | Key name                            |
        +-------------------+-------------------------------------+
        | value             | Value                               |
        +-------------------+-------------------------------------+
    """

    doi = ForeignKeyField(
        DOIEntries, related_name='metadata', column_name='doi')
    key = CharField()
    value = CharField()

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('doi', 'key', 'value')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(DOIInfo, DOIInfo).elastic_mapping_builder(obj)
        obj['doi'] = obj['key'] = obj['value'] = \
            {'type': 'text', 'fields': {'keyword': {
                'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(DOIInfo, self).to_hash(**flags)
        obj['doi'] = unicode_type(self.__data__['doi'])
        obj['key'] = unicode_type(self.__data__['key'])
        obj['value'] = unicode_type(self.__data__['value'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(DOIInfo, self).from_hash(obj)
        self._set_only_if(
            'doi', obj, 'doi',
            lambda: DOIEntries.get(DOIEntries.doi == obj['doi'])
        )
        self._set_only_if(
            'value', obj, 'value', lambda: unicode_type(obj['value'])
        )
        self._set_only_if(
            'key', obj, 'key', lambda: unicode_type(obj['key'])
        )

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(DOIInfo, cls).where_clause(kwargs)
        attrs = ['doi', 'key', 'value']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
