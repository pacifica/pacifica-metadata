#!/usr/bin/python
"""Contains model for Journal."""
from peewee import CharField, FloatField, Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import unicode_type


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

    name = CharField(default='')
    impact_factor = FloatField(default=-1.0)
    website_url = CharField(default='')
    encoding = CharField(default='UTF8')

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(Journals, Journals).elastic_mapping_builder(obj)
        obj['name'] = obj['website_url'] = obj['encoding'] = \
            {'type': 'text', 'fields': {'keyword': {'type': 'keyword', 'ignore_above': 256}}}
        obj['impact_factor'] = {'type': 'float'}

    def to_hash(self, recursion_depth=1):
        """Convert the object to a hash."""
        obj = super(Journals, self).to_hash(recursion_depth)
        obj['_id'] = int(self.id)
        obj['name'] = unicode_type(self.name)
        obj['impact_factor'] = float(self.impact_factor)
        obj['website_url'] = str(self.website_url)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(Journals, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: int(obj['_id']))
        self._set_only_if('name', obj, 'name', lambda: unicode_type(obj['name']))
        self._set_only_if('impact_factor', obj, 'impact_factor',
                          lambda: float(obj['impact_factor']))
        self._set_only_if('website_url', obj, 'website_url',
                          lambda: str(obj['website_url']))
        self._set_only_if('encoding', obj, 'encoding', lambda: str(obj['encoding']))

    def where_clause(self, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(Journals, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Journals.id, OP.EQ, kwargs['_id'])
        for key in ['name', 'impact_factor', 'website_url', 'encoding']:
            if key in kwargs:
                key_oper = OP.EQ
                if '{0}_operator'.format(key) in kwargs:
                    key_oper = getattr(OP, kwargs['{0}_operator'.format(key)].upper())
                where_clause &= Expression(getattr(Journals, key), key_oper, kwargs[key])
        return where_clause
