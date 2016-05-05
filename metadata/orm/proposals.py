#!/usr/bin/python
"""
Proposals data model
"""
from datetime import datetime
from time import mktime
from peewee import TextField, CharField, DateTimeField, Expression, OP
from metadata.rest.orm import CherryPyAPI

# pylint: disable=too-many-instance-attributes
class Proposals(CherryPyAPI):
    """
    Proposals data model
    """
    title = TextField(default="")
    abstract = TextField(default="")
    science_theme = CharField(default="")
    proposal_type = CharField(default="")
    submitted_date = DateTimeField(default=datetime.now)
    accepted_date = DateTimeField(default=datetime.now)
    actual_start_date = DateTimeField(default=datetime.now)
    actual_end_date = DateTimeField(default=datetime.now)

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Proposals, Proposals).elastic_mapping_builder(obj)
        obj['title'] = obj['abstract'] = obj['science_theme'] = obj['proposal_type'] = \
        {'type': 'string'}
        obj['submitted_date'] = obj['accepted_date'] = obj['actual_start_date'] = \
        obj['actual_end_date'] = {'type': 'date', 'format': 'epoch_second'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Proposals, self).to_hash()
        obj['_id'] = int(self.id)
        obj['title'] = str(self.title)
        obj['abstract'] = str(self.abstract)
        obj['science_theme'] = str(self.science_theme)
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
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = int(obj['_id'])
            # pylint: enable=invalid-name
        if 'title' in obj:
            self.title = str(obj['title'])
        if 'abstract' in obj:
            self.abstract = str(obj['abstract'])
        if 'science_theme' in obj:
            self.science_theme = str(obj['science_theme'])
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
        if '_id' in kwargs:
            where_clause &= Expression(Proposals.id, OP.EQ, kwargs['_id'])
        for key in ['title', 'abstract', 'science_theme', 'proposal_type']:
            if key in kwargs:
                where_clause &= Expression(getattr(Proposals, key), OP.EQ, kwargs[key])
        return where_clause
