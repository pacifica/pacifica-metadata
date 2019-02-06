#!/usr/bin/python
# -*- coding: utf-8 -*-
"""FileKeyValue links Files and Keys and Values objects."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.base import DB
from pacifica.metadata.orm.utils import index_hash
from pacifica.metadata.orm.files import Files
from pacifica.metadata.orm.values import Values
from pacifica.metadata.orm.keys import Keys
from pacifica.metadata.rest.orm import CherryPyAPI


class FileKeyValue(CherryPyAPI):
    """
    FileKeyValue attributes are foreign keys.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | file              | Link to the File model              |
        +-------------------+-------------------------------------+
        | key               | Link to the Key model               |
        +-------------------+-------------------------------------+
        | value             | Link to the Value model             |
        +-------------------+-------------------------------------+
    """

    file = ForeignKeyField(Files, backref='metadata')
    key = ForeignKeyField(Keys, backref='file_links')
    value = ForeignKeyField(Values, backref='file_links')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('file', 'key', 'value')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(FileKeyValue, self).to_hash(**flags)
        obj['_id'] = index_hash(int(self.__data__['key']),
                                int(self.__data__['file']),
                                int(self.__data__['value']))
        obj['file_id'] = int(self.__data__['file'])
        obj['key_id'] = int(self.__data__['key'])
        obj['value_id'] = int(self.__data__['value'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(FileKeyValue, self).from_hash(obj)
        self._set_only_if('file_id', obj, 'file',
                          lambda: Files.get(Files.id == obj['file_id']))
        self._set_only_if('key_id', obj, 'key',
                          lambda: Keys.get(Keys.id == obj['key_id']))
        self._set_only_if('value_id', obj, 'value',
                          lambda: Values.get(Values.id == obj['value_id']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(FileKeyValue, cls).where_clause(kwargs)
        attrs = ['file', 'key', 'value']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
