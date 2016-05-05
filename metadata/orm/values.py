#!/usr/bin/python
"""
Contains the model for metadata values
"""
from peewee import CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Values(CherryPyAPI):
    """
    Values model class for metadata
    """
    value = CharField(default="")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Values, Values).elastic_mapping_builder(obj)
        obj['value'] = {'type': 'string'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Values, self).to_hash()
        obj['_id'] = int(self.id)
        obj['value'] = str(self.value)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash to the object
        """
        super(Values, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = obj['_id']
            # pylint: enable=invalid-name
        if 'value' in obj:
            self.value = obj['value']

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Values, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Values.id, OP.EQ, kwargs['_id'])
        if 'value' in kwargs:
            where_clause &= Expression(Values.value, OP.EQ, kwargs['value'])
        return where_clause
