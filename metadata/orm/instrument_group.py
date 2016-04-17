#!/usr/bin/python
"""
InstrumentGroup links Groups and Instruments and objects.
"""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.base import DB, PacificaModel
from metadata.orm.groups import Groups
from metadata.orm.instruments import Instruments

class InstrumentGroup(PacificaModel):
    """
    InstrumentGroup attributes are foreign keys.
    """
    instrument = ForeignKeyField(Instruments, related_name='groups')
    group = ForeignKeyField(Groups, related_name='members')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        PeeWee meta class contains the database and the primary key.
        """
        database = DB
        primary_key = CompositeKey('instrument', 'group')
    # pylint: enable=too-few-public-methods

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(InstrumentGroup, self).to_hash()
        obj['instrument_id'] = int(self.instrument.instrument_id)
        obj['group_id'] = int(self.group.group_id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash into the object
        """
        super(InstrumentGroup, self).from_hash(obj)
        if 'instrument_id' in obj:
            self.instrument = Instruments.get(Instruments.instrument_id == obj['instrument_id'])
        if 'group_id' in obj:
            self.group = Groups.get(Groups.group_id == obj['group_id'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(InstrumentGroup, self).where_clause(kwargs)
        if 'instrument_id' in kwargs:
            instrument = Instruments.get(Instruments.instrument_id == kwargs['instrument_id'])
            where_clause &= Expression(InstrumentGroup.instrument, OP.EQ, instrument)
        if 'group_id' in kwargs:
            group = Groups.get(Groups.group_id == kwargs['group_id'])
            where_clause &= Expression(InstrumentGroup.group, OP.EQ, group)
        return where_clause

