#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Instrument user relationship."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.utils import index_hash
from pacifica.metadata.orm.users import Users
from pacifica.metadata.orm.instruments import Instruments
from pacifica.metadata.orm.base import DB
from pacifica.metadata.rest.orm import CherryPyAPI

# NOTE: rename to instrument user


class InstrumentUser(CherryPyAPI):
    """
    Relates users and instrument objects.

    Attributes:
        +------------+--------------------------------------------+
        | Name       | Description                                |
        +============+============================================+
        | instrument | Link to the Instrument model               |
        +------------+--------------------------------------------+
        | user       | User who is responsible for the instrument |
        +------------+--------------------------------------------+
    """

    instrument = ForeignKeyField(Instruments, backref='custodians')
    # NOTE: rename to user add relationship
    user = ForeignKeyField(Users, backref='instruments')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('instrument', 'user')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(InstrumentUser, self).to_hash(**flags)
        obj['_id'] = index_hash(int(self.__data__['user']),
                                int(self.__data__['instrument']))
        obj['instrument'] = int(self.__data__['instrument'])
        obj['user'] = int(self.__data__['user'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(InstrumentUser, self).from_hash(obj)
        self._set_only_if(
            'instrument', obj, 'instrument',
            lambda: Instruments.get(Instruments.id == obj['instrument'])
        )
        self._set_only_if(
            'user', obj, 'user',
            lambda: Users.get(Users.id == obj['user'])
        )

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(InstrumentUser, cls).where_clause(kwargs)
        attrs = ['instrument', 'user']
        return cls._where_attr_clause(where_clause, kwargs, attrs)
