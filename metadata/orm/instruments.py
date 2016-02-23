#!/usr/bin/python
"""
Instrument model describing data generators.
"""
from peewee import IntegerField, CharField, Expression, OP
from metadata.orm.base import PacificaModel

class Instruments(PacificaModel):
    """
    Instrument and associated fields.
    """
    instrument_id = IntegerField(default=-1, primary_key=True)
    display_name = CharField(default="")
    instrument_name = CharField(default="")
    name_short = CharField(default="")

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Instruments, self).to_hash()
        obj['instrument_id'] = int(self.instrument_id)
        obj['instrument_name'] = str(self.instrument_name)
        obj['display_name'] = str(self.display_name)
        obj['name_short'] = str(self.name_short)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object.
        """
        super(Instruments, self).from_hash(obj)
        if 'instrument_id' in obj:
            self.instrument_id = int(obj['instrument_id'])
        if 'instrument_name' in obj:
            self.instrument_name = str(obj['instrument_name'])
        if 'display_name' in obj:
            self.display_name = str(obj['display_name'])
        if 'name_short' in obj:
            self.name_short = str(obj['name_short'])

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Instruments, self).where_clause(kwargs)
        for key in ['instrument_id', 'instrument_name', 'display_name',
                    'name_short']:
            if key in kwargs:
                where_clause &= Expression(Instruments.__dict__[key].field, OP.EQ, kwargs[key])
        return where_clause

