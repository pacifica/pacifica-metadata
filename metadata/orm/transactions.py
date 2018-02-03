#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Transactions model."""
from peewee import ForeignKeyField, Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.users import Users
from metadata.orm.proposals import Proposals
from metadata.orm.instruments import Instruments
from metadata.orm.utils import unicode_type, ExtendDateField, date_converts


class Transactions(CherryPyAPI):
    """
    Transactions model class.

    Attributes:
        +-------------------+--------------------------------------+
        | Name              | Description                          |
        +===================+======================================+
        | submitter         | User who submitted the transaction   |
        +-------------------+--------------------------------------+
        | instrument        | Instrument the transaction came from |
        +-------------------+--------------------------------------+
        | proposal          | Proposal the transaction is for      |
        +-------------------+--------------------------------------+
        | suspense_date     | date the transaction is available    |
        +-------------------+--------------------------------------+
    """

    submitter = ForeignKeyField(Users, related_name='transactions')
    instrument = ForeignKeyField(Instruments, related_name='transactions')
    proposal = ForeignKeyField(Proposals, related_name='transactions')
    suspense_date = ExtendDateField(null=True, index=True)

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(Transactions, Transactions).elastic_mapping_builder(obj)
        obj['submitter'] = {'type': 'integer'}
        obj['instrument'] = {'type': 'integer'}
        obj['proposal'] = {'type': 'text', 'fields': {
            'keyword': {'type': 'keyword', 'ignore_above': 256}}}
        obj['suspense_date'] = {'type': 'date', 'format': 'yyyy-mm-dd'}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(Transactions, self).to_hash(**flags)
        obj['_id'] = int(self.id) if self.id is not None else obj['_id']
        obj['submitter'] = int(self._data['submitter'])
        obj['instrument'] = int(self._data['instrument'])
        obj['proposal'] = unicode_type(self._data['proposal'])
        obj['suspense_date'] = str(self.suspense_date.isoformat(
        )) if self.suspense_date is not None else None
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(Transactions, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: int(obj['_id']))
        attr_cls_map = [
            ('submitter', Users),
            ('instrument', Instruments),
            ('proposal', Proposals)
        ]
        for key, obj_cls in attr_cls_map:
            self._set_only_if(
                key, obj, key, lambda o=obj_cls, k=key: o.get(o.id == obj[k]))
        self._set_date_part('suspense_date', obj)

    def _where_date_clause(self, where_clause, kwargs):
        for date in ['suspense_date']:
            if date in kwargs:
                date_obj, date_oper = self._date_operator_compare(
                    date, kwargs, dt_converts=date_converts)
                where_clause &= Expression(
                    getattr(Transactions, date), date_oper, date_obj)
        return where_clause

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(Transactions, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Transactions.id, OP.EQ, kwargs['_id'])
        where_clause = self._where_attr_clause(
            where_clause,
            kwargs,
            [
                'submitter',
                'instrument',
                'proposal'
            ]
        )
        where_clause = self._where_date_clause(where_clause, kwargs)
        return where_clause
