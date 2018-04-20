#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Contains the model for metadata analytical tools."""
from peewee import ForeignKeyField, Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import unicode_type
from metadata.orm.users import Users
from metadata.orm.transactions import Transactions
from metadata.orm.data_release_states import DataReleaseStates


class TransactionRelease(CherryPyAPI):
    """
    Keys model class for data release workflow.

    Attributes:
        +-------------------+-----------------------------------------------+
        | Name              | Description                                   |
        +===================+===============================================+
        | transaction       | transaction to be released                    |
        +-------------------+-----------------------------------------------|
        | release_state     | current data release state of the transaction |
        +-------------------+-----------------------------------------------+
        | person            | person originating the release                |
        +-------------------+-----------------------------------------------+
    """

    person = ForeignKeyField(Users, related_name='releases')
    transaction = ForeignKeyField(Transactions, related_name='users')
    release_state = ForeignKeyField(DataReleaseStates)

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(TransactionRelease, TransactionRelease).elastic_mapping_builder(obj)
        obj['transaction_id'] = obj['person_id'] = obj['release_state_id'] = \
            {'type': 'integer'}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(TransactionRelease, self).to_hash(**flags)
        obj['_id'] = int(self._data['id'])
        obj['transaction_id'] = int(self._data['transaction'])
        obj['release_state_id'] = int(self._data['release_state'])
        # pylint: disable=no-member
        obj['person_id'] = int(self._data['person'])
        # pylint: enable=no-member

        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(TransactionRelease, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: int(obj['_id']))
        if 'transaction_id' in obj:
            self.transaction = Transactions.get(
                Transactions.id == obj['transaction_id'])
        if 'release_state_id' in obj:
            self.release_state = DataReleaseStates.get(
                DataReleaseStates.id == obj['release_state_id'])
        if 'person_id' in obj:
            self.person = Users.get(
                Users.id == obj['person_id'])

    def where_clause(self, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(TransactionRelease, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(
                TransactionRelease.id, OP.EQ, kwargs['_id'])
        if 'transaction_id' in kwargs:
            where_clause &= Expression(
                TransactionRelease.transaction, OP.EQ, kwargs['transaction_id'])
        if 'person_id' in kwargs:
            where_clause &= Expression(
                TransactionRelease.person, OP.EQ, kwargs['person_id'])
        if 'release_state_id' in kwargs:
            where_clause &= Expression(
                TransactionRelease.release_state, OP.EQ, kwargs['release_state_id'])
        return where_clause
