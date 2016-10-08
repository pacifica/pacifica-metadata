#!/usr/bin/python
"""
Contains the model for metadata analytical tools
"""
from peewee import CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class AnalyticalTools(CherryPyAPI):
    """
    Keys model class for metadata

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | name              | generic tool name                   |
        +-------------------+-------------------------------------+
        | encoding          | encoding for the name               |
        +-------------------+-------------------------------------+
    """
    name = CharField(default="")
    encoding = CharField(default="UTF8")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(AnalyticalTools, AnalyticalTools).elastic_mapping_builder(obj)
        obj['name'] = obj['encoding'] = {'type': 'string'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(AnalyticalTools, self).to_hash()
        obj['_id'] = int(self.id)
        obj['name'] = unicode(self.name)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash to the object
        """
        super(AnalyticalTools, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = obj['_id']
            # pylint: enable=invalid-name
        if 'name' in obj:
            self.name = unicode(obj['name'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(AnalyticalTools, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(AnalyticalTools.id, OP.EQ, kwargs['_id'])
        if 'name' in kwargs:
            where_clause &= Expression(AnalyticalTools.name, OP.EQ, kwargs['name'])
        if 'encoding' in kwargs:
            where_clause &= Expression(AnalyticalTools.encoding, OP.EQ, kwargs['encoding'])
        return where_clause
