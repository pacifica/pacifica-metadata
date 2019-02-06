#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Instrument custodian relationship."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.utils import index_hash
from pacifica.metadata.orm.users import Users
from pacifica.metadata.orm.instruments import Instruments
from pacifica.metadata.orm.base import DB
from pacifica.metadata.rest.orm import CherryPyAPI


class InstrumentCustodian(CherryPyAPI):
    """
    Relates proposals and instrument objects.

    Attributes:
        +------------+--------------------------------------------+
        | Name       | Description                                |
        +============+============================================+
        | instrument | Link to the Instrument model               |
        +------------+--------------------------------------------+
        | custodian  | User who is responsible for the instrument |
        +------------+--------------------------------------------+
    """

    instrument = ForeignKeyField(Instruments, backref='custodians')
    custodian = ForeignKeyField(Users, backref='instruments')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('instrument', 'custodian')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(InstrumentCustodian, self).to_hash(**flags)
        obj['_id'] = index_hash(int(self.__data__['custodian']),
                                int(self.__data__['instrument']))
        obj['instrument_id'] = int(self.__data__['instrument'])
        obj['custodian_id'] = int(self.__data__['custodian'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(InstrumentCustodian, self).from_hash(obj)
        self._set_only_if(
            'instrument_id', obj, 'instrument', lambda: Instruments.get(
                Instruments.id == obj['instrument_id'])
        )
        self._set_only_if(
            'custodian_id', obj, 'custodian', lambda: Users.get(
                Users.id == obj['custodian_id'])
        )

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(InstrumentCustodian, cls).where_clause(kwargs)
        attrs = ['instrument', 'custodian']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
