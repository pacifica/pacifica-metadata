#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Proposals data model."""
from peewee import TextField, CharField, Expression, OP
from pacifica.metadata.rest.orm import CherryPyAPI
from pacifica.metadata.orm.utils import ExtendDateTimeField, ExtendDateField
from pacifica.metadata.orm.utils import date_converts, datetime_now_nomicrosecond
from pacifica.metadata.orm.utils import unicode_type


# pylint: disable=too-many-instance-attributes
class Proposals(CherryPyAPI):
    """
    Proposals data model.

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
        | suspense_date     | date the proposal is made available |
        +-------------------+-------------------------------------+
        | encoding          | encoding of the other text attrs    |
        +-------------------+-------------------------------------+
    """

    id = CharField(primary_key=True)
    title = TextField(default='', index=True)
    short_name = CharField(null=True, default='', index=True)
    abstract = TextField(null=True, default='')
    science_theme = CharField(null=True)
    proposal_type = CharField(null=True, default='')
    submitted_date = ExtendDateTimeField(
        default=datetime_now_nomicrosecond, index=True)
    accepted_date = ExtendDateField(null=True, index=True)
    actual_start_date = ExtendDateField(null=True, index=True)
    actual_end_date = ExtendDateField(null=True, index=True)
    closed_date = ExtendDateField(null=True, index=True)
    suspense_date = ExtendDateField(null=True, index=True)
    encoding = CharField(default='UTF8')

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        exclude_text = flags.get('exclude_text', False)
        obj = super(Proposals, self).to_hash(**flags)
        obj['_id'] = unicode_type(self.id)
        obj['title'] = unicode_type(self.title)
        obj['short_name'] = unicode_type(self.short_name)

        def _set_only_if(attr, expr, true_value, else_func):
            obj[attr] = true_value if expr else else_func()
        obj['science_theme'] = unicode_type(self.science_theme)
        obj['proposal_type'] = unicode_type(self.proposal_type)
        obj['submitted_date'] = self.submitted_date.isoformat()
        # pylint: disable=unnecessary-lambda
        _set_only_if('abstract', exclude_text, None,
                     lambda: unicode_type(self.abstract))
        _set_only_if(
            'actual_start_date',
            self.actual_start_date is None,
            None,
            lambda: self.actual_start_date.isoformat()
        )
        _set_only_if('accepted_date', self.accepted_date is None,
                     None, lambda: self.accepted_date.isoformat())
        _set_only_if('actual_end_date', self.actual_end_date is None,
                     None, lambda: self.actual_end_date.isoformat())
        _set_only_if('closed_date', self.closed_date is None,
                     None, lambda: self.closed_date.isoformat())
        _set_only_if('suspense_date', self.suspense_date is None,
                     None, lambda: self.suspense_date.isoformat())
        # pylint: enable=unnecessary-lambda
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(Proposals, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: unicode_type(obj['_id']))
        self._set_only_if('title', obj, 'title',
                          lambda: unicode_type(obj['title']))
        self._set_only_if('short_name', obj, 'short_name',
                          lambda: unicode_type(obj['short_name']))
        self._set_only_if('abstract', obj, 'abstract',
                          lambda: unicode_type(obj['abstract']))
        self._set_only_if('science_theme', obj, 'science_theme',
                          lambda: unicode_type(obj['science_theme']))
        self._set_only_if('proposal_type', obj, 'proposal_type',
                          lambda: unicode_type(obj['proposal_type']))
        self._set_only_if('encoding', obj, 'encoding',
                          lambda: str(obj['encoding']))
        self._set_datetime_part('submitted_date', obj)
        self._set_date_part('accepted_date', obj)
        self._set_date_part('actual_start_date', obj)
        self._set_date_part('actual_end_date', obj)
        self._set_date_part('closed_date', obj)
        self._set_date_part('suspense_date', obj)

    @classmethod
    def _where_date_clause(cls, where_clause, kwargs):
        date_keys = [
            'accepted_date',
            'actual_start_date',
            'actual_end_date',
            'closed_date',
            'suspense_date'
        ]
        for date_key in date_keys:
            if date_key in kwargs:
                date_obj, date_oper = cls._date_operator_compare(
                    date_key, kwargs, date_converts)
                where_clause &= Expression(
                    getattr(Proposals, date_key), date_oper, date_obj)
        return where_clause

    @classmethod
    def _where_datetime_clause(cls, where_clause, kwargs):
        for date_key in ['submitted_date']:
            if date_key in kwargs:
                date_obj, date_oper = cls._date_operator_compare(
                    date_key, kwargs)
                where_clause &= Expression(
                    getattr(Proposals, date_key), date_oper, date_obj)
        return where_clause

    @classmethod
    def where_clause(cls, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(Proposals, cls).where_clause(kwargs)
        where_clause = cls._where_date_clause(where_clause, kwargs)
        where_clause = cls._where_datetime_clause(where_clause, kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Proposals.id, OP.EQ, kwargs['_id'])
        return cls._where_attr_clause(
            where_clause,
            kwargs,
            [
                'title',
                'short_name',
                'abstract',
                'science_theme',
                'proposal_type',
                'encoding'
            ]
        )
