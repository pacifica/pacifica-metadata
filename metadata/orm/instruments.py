#!/usr/bin/python
"""
Instrument model describing data generators.
"""
from peewee import CharField, Expression, OP, BooleanField
from metadata.rest.orm import CherryPyAPI

class Instruments(CherryPyAPI):
    """
    Instrument and associated fields.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | display_name      | Long display string for web sites   |
        +-------------------+-------------------------------------+
        | instrument_name   | Machine parsable display name       |
        +-------------------+-------------------------------------+
        | name_short        | Short version used in lists         |
        +-------------------+-------------------------------------+
        | active            | whether the instrument is active    |
        +-------------------+-------------------------------------+
        | encoding          | encoding for the various name attrs |
        +-------------------+-------------------------------------+
    """
    display_name = CharField(default="")
    instrument_name = CharField(default="")
    name_short = CharField(default="")
    active = BooleanField(default=False)
    encoding = CharField(default="UTF8")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Instruments, Instruments).elastic_mapping_builder(obj)
        obj['display_name'] = obj['instrument_name'] = obj['name_short'] = \
        obj['encoding'] = {'type': 'string'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Instruments, self).to_hash()
        obj['_id'] = self.id
        obj['instrument_name'] = unicode(self.instrument_name)
        obj['display_name'] = unicode(self.display_name)
        obj['name_short'] = unicode(self.name_short)
        obj['active'] = bool(self.active)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object.
        """
        super(Instruments, self).from_hash(obj)
        # pylint: disable=invalid-name
        if '_id' in obj:
            self.id = int(obj['_id'])
        # pylint: enable=invalid-name
        if 'instrument_name' in obj:
            self.instrument_name = unicode(obj['instrument_name'])
        if 'display_name' in obj:
            self.display_name = unicode(obj['display_name'])
        if 'name_short' in obj:
            self.name_short = unicode(obj['name_short'])
        if 'active' in obj:
            self.active = bool(obj['active'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Instruments, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Instruments.id, OP.EQ, kwargs['_id'])
        for key in ['instrument_name', 'display_name', 'name_short', 'active',
                    'encoding']:
            if key in kwargs:
                where_clause &= Expression(getattr(Instruments, key), OP.EQ, kwargs[key])
        return where_clause
