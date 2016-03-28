#!/usr/bin/python
"""
Instrument custodian relationship
"""
from peewee import ForeignKeyField, Expression, OP, CompositeKey
from metadata.orm.users import Users
from metadata.orm.instruments import Instruments
from metadata.orm.base import DB, PacificaModel

class InstrumentCustodian(PacificaModel):
    """
    Relates proposals and instrument objects.
    """
    instrument = ForeignKeyField(Instruments, related_name='custodians')
    custodian = ForeignKeyField(Users, related_name='instruments')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        PeeWee meta class contains the database and the primary key.
        """
        database = DB
        primary_key = CompositeKey('instrument', 'custodian')
    # pylint: enable=too-few-public-methods

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(InstrumentCustodian, self).to_hash()
        obj['instrument_id'] = int(self.instrument.instrument_id)
        obj['person_id'] = int(self.custodian.person_id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash into the object
        """
        super(InstrumentCustodian, self).from_hash(obj)
        if 'instrument_id' in obj:
            self.instrument = Instruments.get(Instruments.instrument_id == obj['instrument_id'])
        if 'person_id' in obj:
            self.custodian = Users.get(Users.person_id == obj['person_id'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(InstrumentCustodian, self).where_clause(kwargs)
        if 'instrument_id' in kwargs:
            instrument = Instruments.get(Instruments.instrument_id == kwargs['instrument_id'])
            where_clause &= Expression(InstrumentCustodian.instrument, OP.EQ, instrument)
        if 'person_id' in kwargs:
            user = Users.get(Users.person_id == kwargs['person_id'])
            where_clause &= Expression(InstrumentCustodian.custodian, OP.EQ, user)
        return where_clause
