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
        obj['_id'] = int(self.id)
        obj['transaction_id'] = int(self.transaction.id)
        # pylint: disable=no-member
        obj['release_state'] = unicode_type(self.release_state.name)
        obj['release_state_display_name'] = unicode_type(
            self.release_state.display_name)
        obj['person_id'] = int(self.person.id)
        # pylint: enable=no-member

        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(TransactionRelease, self).from_hash(obj)
        if 'transaction_id' in obj:
            self.transaction = obj['transaction_id']
        if 'release_state' in obj:
            self.release_state = unicode_type(obj['release_state'])
        if 'person_id' in obj:
            self.person = unicode_type(obj['person_id'])

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
        if 'release_state' in kwargs:
            where_clause &= Expression(
                TransactionRelease.release_state, OP.EQ, kwargs['release_state'])
        return where_clause
