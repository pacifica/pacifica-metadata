#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Contains the model for metadata analytical tools."""
from peewee import ForeignKeyField, Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.users import Users
from metadata.orm.transactions import Transactions


class TransactionRelease(CherryPyAPI):
    """
    TransactionRelease model class for data release workflow.

    Attributes:
        +-------------------+-----------------------------------------------+
        | Name              | Description                                   |
        +===================+===============================================+
        | transaction       | transaction to be released                    |
        +-------------------+-----------------------------------------------|
        | authorized_person | authorized person originating the release     |
        +-------------------+-----------------------------------------------+
    """

    authorized_person = ForeignKeyField(
        Users, related_name='authorized_releases')
    transaction = ForeignKeyField(Transactions, related_name='release_state')

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(TransactionRelease, TransactionRelease).elastic_mapping_builder(obj)
        obj['transaction_id'] = obj['person_id'] = {'type': 'integer'}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(TransactionRelease, self).to_hash(**flags)
        obj['_id'] = int(self.__data__['id'])
        obj['transaction_id'] = int(self.__data__['transaction'])
        # pylint: disable=no-member
        obj['authorized_person_id'] = int(self.__data__['authorized_person'])
        # pylint: enable=no-member

        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(TransactionRelease, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: int(obj['_id']))
        self._set_only_if('transaction_id', obj, 'transaction', lambda: Transactions.get(
            Transactions.id == obj['transaction_id']))
        self._set_only_if('authorized_person_id', obj, 'authorized_person', lambda: Users.get(
            Users.id == obj['authorized_person_id']))

    def where_clause(self, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(TransactionRelease, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(
                TransactionRelease.id, OP.EQ, kwargs['_id'])
        return self._where_attr_clause(where_clause, kwargs, ['authorized_person', 'transaction'])
