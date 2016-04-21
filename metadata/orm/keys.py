#!/usr/bin/python
"""
Contains the model for metadata keys
"""
from peewee import IntegerField, CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Keys(CherryPyAPI):
    """
    Keys model class for metadata
    """
    key_id = IntegerField(default=-1, primary_key=True)
    key = CharField(default="")

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Keys, self).to_hash()
        obj['key_id'] = int(self.key_id)
        obj['key'] = str(self.key)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash to the object
        """
        super(Keys, self).from_hash(obj)
        if 'key_id' in obj:
            self.key_id = obj['key_id']
        if 'key' in obj:
            self.key = obj['key']

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Keys, self).where_clause(kwargs)
        for key in ['key_id', 'key']:
            if key in kwargs:
                where_clause &= Expression(getattr(Keys, key), OP.EQ, kwargs[key])
        return where_clause
