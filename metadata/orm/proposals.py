#!/usr/bin/python
"""
Proposals data model
"""
from datetime import datetime
from time import mktime
from peewee import IntegerField, TextField, CharField, DateTimeField, Expression, OP
from metadata.orm.base import PacificaModel

# pylint: disable=too-many-instance-attributes
class Proposals(PacificaModel):
    """
    Proposals data model
    """
    proposal_id = CharField(default="", primary_key=True)
    title = TextField(default="")
    abstract = TextField(default="")
    science_theme = CharField(default="")
    science_theme_id = IntegerField(default=-1)
    proposal_type = CharField(default="")
    submitted_date = DateTimeField(default=datetime.now)
    accepted_date = DateTimeField(default=datetime.now)
    actual_start_date = DateTimeField(default=datetime.now)
    actual_end_date = DateTimeField(default=datetime.now)

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Proposals, self).to_hash()
        obj['proposal_id'] = int(self.proposal_id)
        obj['title'] = str(self.title)
        obj['abstract'] = str(self.abstract)
        obj['science_theme'] = str(self.science_theme)
        obj['science_theme_id'] = int(self.science_theme_id)
        obj['proposal_type'] = str(self.proposal_type)
        obj['submitted_date'] = int(mktime(self.submitted_date.timetuple()))
        obj['accepted_date'] = int(mktime(self.accepted_date.timetuple()))
        obj['actual_start_date'] = int(mktime(self.actual_start_date.timetuple()))
        obj['actual_end_date'] = int(mktime(self.actual_end_date.timetuple()))
        return obj

    def from_hash(self, obj):
        """
        Converts the hash to the object
        """
        super(Proposals, self).from_hash(obj)
        if 'proposal_id' in obj:
            self.proposal_id = int(obj['proposal_id'])
        if 'title' in obj:
            self.title = str(obj['title'])
        if 'abstract' in obj:
            self.abstract = str(obj['abstract'])
        if 'science_theme' in obj:
            self.science_theme = str(obj['science_theme'])
        if 'science_theme_id' in obj:
            self.science_theme_id = int(obj['science_theme_id'])
        if 'proposal_type' in obj:
            self.proposal_type = str(obj['proposal_type'])
        if 'submitted_date' in obj:
            self.submitted_date = datetime.fromtimestamp(int(obj['submitted_date']))
        if 'accepted_date' in obj:
            self.accepted_date = datetime.fromtimestamp(int(obj['accepted_date']))
        if 'actual_start_date' in obj:
            self.actual_start_date = datetime.fromtimestamp(int(obj['actual_start_date']))
        if 'actual_end_date' in obj:
            self.actual_end_date = datetime.fromtimestamp(int(obj['actual_end_date']))

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Proposals, self).where_clause(kwargs)
        for date_key in ['submitted_date', 'accepted_date',
                         'actual_start_date', 'actual_end_date']:
            if date_key in kwargs:
                date_obj = datetime.fromtimestamp(kwargs[date_key])
                where_clause &= Expression(getattr(Proposals, date_key), OP.EQ, date_obj)
        for key in ['proposal_id', 'title', 'abstract', 'science_theme', 'science_theme_id'
                    'proposal_type']:
            if key in kwargs:
                where_clause &= Expression(getattr(Proposals, key), OP.EQ, kwargs[key])
        return where_clause
