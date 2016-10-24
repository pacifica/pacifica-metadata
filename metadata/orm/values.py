#!/usr/bin/python
"""
Contains the model for metadata values
"""
from peewee import CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Values(CherryPyAPI):
    """
    Values model class for metadata

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | value             | generic value for some metadata     |
        +-------------------+-------------------------------------+
        | encoding          | language encoding of the value      |
        +-------------------+-------------------------------------+
    """
    value = CharField(default="")
    encoding = CharField(default="UTF8")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Values, Values).elastic_mapping_builder(obj)
        obj['value'] = obj['encoding'] = {'type': 'string'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Values, self).to_hash()
        obj['_id'] = int(self.id)
        obj['value'] = unicode(self.value)
        obj['encoding'] = str(self.encoding)
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
            self.value = unicode(obj['value'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Values, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Values.id, OP.EQ, kwargs['_id'])
        for key in ['value', 'encoding']:
            if key in kwargs:
                key_oper = OP.EQ
                if "%s_operator"%(key) in kwargs:
                    key_oper = getattr(OP, kwargs["%s_operator"%(key)])
                where_clause &= Expression(getattr(Values, key), key_oper, kwargs[key])
        return where_clause
