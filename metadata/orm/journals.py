#!/usr/bin/python
"""
Contains model for Journal
"""
from peewee import IntegerField, CharField, FloatField, Expression, OP
from metadata.orm.base import PacificaModel

class Journals(PacificaModel):
    """
    Journal model and associated fields.
    """
    journal_id = IntegerField(default=-1, primary_key=True)
    journal_name = CharField(default="")
    impact_factor = FloatField(default=-1.0)
    website_url = CharField(default="")

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Journals, self).to_hash()
        obj['journal_id'] = int(self.journal_id)
        obj['journal_name'] = str(self.journal_name)
        obj['impact_factor'] = float(self.impact_factor)
        obj['website_url'] = str(self.website_url)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object.
        """
        super(Journals, self).from_hash(obj)
        if 'journal_id' in obj:
            self.journal_id = int(obj['journal_id'])
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
        for key in ['journal_id', 'journal_name', 'impact_factor',
                    'website_url']:
            if key in kwargs:
                where_clause &= Expression(Journals.__dict__[key].field, OP.EQ, kwargs[key])
        return where_clause

