#!/usr/bin/python
"""
Instrument model describing data generators.
"""
from peewee import CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Instruments(CherryPyAPI):
    """
    Instrument and associated fields.
    """
    display_name = CharField(default="")
    instrument_name = CharField(default="")
    name_short = CharField(default="")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Instruments, Instruments).elastic_mapping_builder(obj)
        obj['display_name'] = obj['instrument_name'] = obj['name_short'] = \
        {'type': 'string'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Instruments, self).to_hash()
        obj['_id'] = int(self.id)
        obj['instrument_name'] = str(self.instrument_name)
        obj['display_name'] = str(self.display_name)
        obj['name_short'] = str(self.name_short)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object.
        """
        super(Instruments, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = int(obj['_id'])
            # pylint: enable=invalid-name
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
        if '_id' in kwargs:
            where_clause &= Expression(Instruments.id, OP.EQ, kwargs['_id'])
        for key in ['instrument_name', 'display_name', 'name_short']:
            if key in kwargs:
                where_clause &= Expression(getattr(Instruments, key), OP.EQ, kwargs[key])
        return where_clause

