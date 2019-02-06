#!/usr/bin/python
# -*- coding: utf-8 -*-
"""InstrumentGroup links Groups and Instruments and objects."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.utils import index_hash
from pacifica.metadata.orm.base import DB
from pacifica.metadata.rest.orm import CherryPyAPI
from pacifica.metadata.orm.groups import Groups
from pacifica.metadata.orm.instruments import Instruments


class InstrumentGroup(CherryPyAPI):
    """
    InstrumentGroup attributes are foreign keys.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | instrument        | Link to the Instrument model        |
        +-------------------+-------------------------------------+
        | group             | Link to the Group model             |
        +-------------------+-------------------------------------+
    """

    instrument = ForeignKeyField(Instruments, backref='groups')
    group = ForeignKeyField(Groups, backref='instrument_members')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('instrument', 'group')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(InstrumentGroup, self).to_hash(**flags)
        obj['_id'] = index_hash(int(self.__data__['group']),
                                int(self.__data__['instrument']))
        obj['instrument_id'] = int(self.__data__['instrument'])
        obj['group_id'] = int(self.__data__['group'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(InstrumentGroup, self).from_hash(obj)
        self._set_only_if('instrument_id', obj, 'instrument',
                          lambda: Instruments.get(Instruments.id == obj['instrument_id']))
        self._set_only_if('group_id', obj, 'group',
                          lambda: Groups.get(Groups.id == obj['group_id']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(InstrumentGroup, cls).where_clause(kwargs)
        attrs = ['instrument', 'group']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
