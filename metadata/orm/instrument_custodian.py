#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Instrument custodian relationship."""
from peewee import ForeignKeyField, Expression, OP, CompositeKey
from metadata.orm.utils import index_hash
from metadata.orm.users import Users
from metadata.orm.instruments import Instruments
from metadata.orm.base import DB
from metadata.rest.orm import CherryPyAPI


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

    instrument = ForeignKeyField(Instruments, related_name='custodians')
    custodian = ForeignKeyField(Users, related_name='instruments')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('instrument', 'custodian')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(InstrumentCustodian, InstrumentCustodian).elastic_mapping_builder(obj)
        obj['instrument_id'] = obj['custodian_id'] = {'type': 'integer'}

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
        if 'instrument_id' in obj:
            self.instrument = Instruments.get(
                Instruments.id == obj['instrument_id'])
        if 'custodian_id' in obj:
            self.custodian = Users.get(Users.id == obj['custodian_id'])

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(InstrumentCustodian, self).where_clause(kwargs)
        if 'instrument_id' in kwargs:
            instrument = int(kwargs['instrument_id'])
            where_clause &= Expression(
                InstrumentCustodian.instrument, OP.EQ, instrument)
        if 'custodian_id' in kwargs:
            user = int(kwargs['custodian_id'])
            where_clause &= Expression(
                InstrumentCustodian.custodian, OP.EQ, user)
        return where_clause
