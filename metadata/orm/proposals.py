#!/usr/bin/python
"""
Proposals data model
"""
from peewee import TextField, CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import ExtendDateTimeField, ExtendDateField
from metadata.orm.utils import date_converts, datetime_now_nomicrosecond

# pylint: disable=too-many-instance-attributes
class Proposals(CherryPyAPI):
    """
    Proposals data model

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | title             | Title of the proposal               |
        +-------------------+-------------------------------------+
        | abstract          | Long abstract of the proposal       |
        +-------------------+-------------------------------------+
        | science_theme     | science group or theme assigned to  |
        +-------------------+-------------------------------------+
        | proposal_type     | kind or type of proposal            |
        +-------------------+-------------------------------------+
        | submitted_date    | date proposal entered the system    |
        +-------------------+-------------------------------------+
        | accepted_date     | date proposal was accepted          |
        +-------------------+-------------------------------------+
        | actual_start_date | date the proposal was started       |
        +-------------------+-------------------------------------+
        | actual_end_date   | date the proposal was ended         |
        +-------------------+-------------------------------------+
        | closed_date       | date the proposal was terminated    |
        +-------------------+-------------------------------------+
        | encoding          | encoding of the other text attrs    |
        +-------------------+-------------------------------------+
    """
    id = CharField(primary_key=True)
    title = TextField(default="")
    abstract = TextField(default="")
    science_theme = CharField(null=True)
    proposal_type = CharField(default="")
    submitted_date = ExtendDateTimeField(default=datetime_now_nomicrosecond)
    accepted_date = ExtendDateField(null=True)
    actual_start_date = ExtendDateField(null=True)
    actual_end_date = ExtendDateField(null=True)
    closed_date = ExtendDateField(null=True)
    encoding = CharField(default="UTF8")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Proposals, Proposals).elastic_mapping_builder(obj)
        obj['title'] = obj['abstract'] = obj['science_theme'] = obj['proposal_type'] = \
        obj['encoding'] = {'type': 'string'}

        obj['submitted_date'] = \
        {'type': 'date', 'format': "yyyy-mm-dd'T'HH:mm:ss"}

        obj['actual_start_date'] = obj['accepted_date'] = \
        obj['actual_end_date'] = obj['closed_date'] = \
        {'type': 'date', 'format': "yyyy-mm-dd"}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Proposals, self).to_hash()
        obj['_id'] = unicode(self.id)
        obj['title'] = unicode(self.title)
        obj['abstract'] = unicode(self.abstract)
        obj['science_theme'] = unicode(self.science_theme)
        obj['proposal_type'] = unicode(self.proposal_type)
        obj['submitted_date'] = self.submitted_date.isoformat()
        obj['actual_start_date'] = self.actual_start_date.isoformat() \
        if self.actual_start_date is not None else None
        obj['accepted_date'] = self.accepted_date.isoformat() \
        if self.accepted_date is not None else None
        obj['actual_end_date'] = self.actual_end_date.isoformat() \
        if self.actual_end_date is not None else None
        obj['closed_date'] = self.closed_date.isoformat() \
        if self.closed_date is not None else None
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash to the object
        """
        super(Proposals, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: unicode(obj['_id']))
        self._set_only_if('title', obj, 'title', lambda: unicode(obj['title']))
        self._set_only_if('abstract', obj, 'abstract', lambda: unicode(obj['abstract']))
        self._set_only_if('science_theme', obj, 'science_theme',
                          lambda: unicode(obj['science_theme'])
                         )
        self._set_only_if('proposal_type', obj, 'proposal_type',
                          lambda: unicode(obj['proposal_type'])
                         )
        self._set_only_if('encoding', obj, 'encoding', lambda: str(obj['encoding']))
        self._set_datetime_part('submitted_date', obj)
        self._set_date_part('accepted_date', obj)
        self._set_date_part('actual_start_date', obj)
        self._set_date_part('actual_end_date', obj)
        self._set_date_part('closed_date', obj)

    def _where_date_clause(self, where_clause, kwargs):
        date_keys = ['accepted_date', 'actual_start_date', 'actual_end_date']
        for date_key in date_keys:
            if date_key in kwargs:
                date_obj, date_oper = self._date_operator_compare(date_key, kwargs, date_converts)
                where_clause &= Expression(getattr(Proposals, date_key), date_oper, date_obj)
        return where_clause

    def _where_datetime_clause(self, where_clause, kwargs):
        for date_key in ['submitted_date']:
            if date_key in kwargs:
                date_obj, date_oper = self._date_operator_compare(date_key, kwargs)
                where_clause &= Expression(getattr(Proposals, date_key), date_oper, date_obj)
        return where_clause

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Proposals, self).where_clause(kwargs)
        where_clause = self._where_date_clause(where_clause, kwargs)
        where_clause = self._where_datetime_clause(where_clause, kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Proposals.id, OP.EQ, kwargs['_id'])
        for key in ['title', 'abstract', 'science_theme', 'proposal_type', 'encoding']:
            if key in kwargs:
                key_oper = OP.EQ
                if "%s_operator"%(key) in kwargs:
                    key_oper = getattr(OP, kwargs["%s_operator"%(key)])
                where_clause &= Expression(getattr(Proposals, key), key_oper, kwargs[key])
        return where_clause
