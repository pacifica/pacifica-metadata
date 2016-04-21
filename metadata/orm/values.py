#!/usr/bin/python
"""
Contains the model for metadata values
"""
from peewee import IntegerField, CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Values(CherryPyAPI):
    """
    Values model class for metadata
    """
    value_id = IntegerField(default=-1, primary_key=True)
    value = CharField(default="")

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Values, self).to_hash()
        obj['value_id'] = int(self.value_id)
        obj['value'] = str(self.value)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash to the object
        """
        super(Values, self).from_hash(obj)
        if 'value_id' in obj:
            self.value_id = obj['value_id']
        if 'value' in obj:
            self.value = obj['value']

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Values, self).where_clause(kwargs)
        for key in ['value_id', 'value']:
            if key in kwargs:
                where_clause &= Expression(getattr(Values, key), OP.EQ, kwargs[key])
        return where_clause
