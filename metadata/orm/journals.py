#!/usr/bin/python
"""
Contains model for Journal
"""
from peewee import CharField, FloatField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Journals(CherryPyAPI):
    """
    Journal model and associated fields.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | name              | name of the journal                 |
        +-------------------+-------------------------------------+
        | author            | impact factor of the journal        |
        +-------------------+-------------------------------------+
        | website_url       | website for the journal (optional)  |
        +-------------------+-------------------------------------+
        | encoding          | language encoding for the name      |
        +-------------------+-------------------------------------+
    """
    name = CharField(default="")
    impact_factor = FloatField(default=-1.0)
    website_url = CharField(default="")
    encoding = CharField(default="UTF8")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Journals, Journals).elastic_mapping_builder(obj)
        obj['name'] = obj['website_url'] = obj['encoding'] = {'type': 'string'}
        obj['impact_factor'] = {'type': 'float'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Journals, self).to_hash()
        obj['_id'] = int(self.id)
        obj['name'] = unicode(self.name)
        obj['impact_factor'] = float(self.impact_factor)
        obj['website_url'] = str(self.website_url)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object.
        """
        super(Journals, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = int(obj['_id'])
            # pylint: enable=invalid-name
        if 'name' in obj:
            self.name = unicode(obj['name'])
        if 'impact_factor' in obj:
            self.impact_factor = float(obj['impact_factor'])
        if 'website_url' in obj:
            self.website_url = str(obj['website_url'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Journals, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Journals.id, OP.EQ, kwargs['_id'])
        for key in ['name', 'impact_factor', 'website_url', 'encoding']:
            if key in kwargs:
                key_oper = OP.EQ
                if "%s_operator"%(key) in kwargs:
                    key_oper = getattr(OP, kwargs["%s_operator"%(key)])
                where_clause &= Expression(getattr(Journals, key), key_oper, kwargs[key])
        return where_clause
