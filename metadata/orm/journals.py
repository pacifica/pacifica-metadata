#!/usr/bin/python
"""
Contains model for Journal
"""
from peewee import CharField, FloatField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Journals(CherryPyAPI):
    """
    Journal model and associated fields.
    """
    journal_name = CharField(default="")
    impact_factor = FloatField(default=-1.0)
    website_url = CharField(default="")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Journals, Journals).elastic_mapping_builder(obj)
        obj['journal_name'] = obj['website_url'] = {'type': 'string'}
        obj['impact_factor'] = {'type': 'float'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Journals, self).to_hash()
        obj['_id'] = int(self.id)
        obj['journal_name'] = str(self.journal_name)
        obj['impact_factor'] = float(self.impact_factor)
        obj['website_url'] = str(self.website_url)
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
        if 'journal_name' in obj:
            self.journal_name = str(obj['journal_name'])
        if 'impact_factor' in obj:
            self.impact_factor = float(obj['impact_factor'])
        if 'website_url' in obj:
            self.website_url = str(obj['website_url'])

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Journals, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Journals.id, OP.EQ, kwargs['_id'])
        for key in ['journal_name', 'impact_factor', 'website_url']:
            if key in kwargs:
                where_clause &= Expression(getattr(Journals, key), OP.EQ, kwargs[key])
        return where_clause
