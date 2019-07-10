#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Datasets model."""
from peewee import TextField, CharField, Expression
from ..rest.orm import CherryPyAPI
from .utils import unicode_type, ExtendDateField, date_converts


class Datasets(CherryPyAPI):
    """
    Datasets model class.

    Attributes:
        +-------------------+--------------------------------------+
        | Name              | Description                          |
        +===================+======================================+
        | description       | Description of the dataset           |
        +-------------------+--------------------------------------+
        | display_name      | dataset display name                 |
        +-------------------+--------------------------------------+
        | suspense_date     | date the dataset is available        |
        +-------------------+--------------------------------------+
    """

    description = TextField(null=True)
    display_name = CharField(default='', index=True)
    suspense_date = ExtendDateField(null=True, index=True)

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(Datasets, self).to_hash(**flags)
        obj['_id'] = int(self.id) if self.id is not None else obj['_id']
        for attr in ['display_name', 'description']:
            obj[attr] = unicode_type(getattr(self, attr))
        obj['suspense_date'] = str(self.suspense_date.isoformat(
        )) if self.suspense_date is not None else None
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(Datasets, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: int(obj['_id']))
        for attr in ['display_name', 'description']:
            self._set_only_if(
                attr, obj, attr, lambda o=obj, a=attr: unicode_type(o[a])
            )
        self._set_date_part('suspense_date', obj)

    @classmethod
    def _where_date_clause(cls, where_clause, kwargs):
        for date in ['suspense_date']:
            if date in kwargs:
                date_obj, date_oper = cls._date_operator_compare(
                    date, kwargs, dt_converts=date_converts)
                where_clause &= Expression(
                    getattr(Datasets, date), date_oper, date_obj)
        return where_clause

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(Datasets, cls).where_clause(kwargs)
        where_clause = cls._where_date_clause(where_clause, kwargs)
        return cls._where_attr_clause(
            where_clause, kwargs, ['description', 'display_name']
        )
