#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Contains the model for metadata analytical tools."""
from peewee import ForeignKeyField
from pacifica.metadata.rest.orm import CherryPyAPI
from pacifica.metadata.orm.users import Users
from pacifica.metadata.orm.transactions import Transactions


class TransactionRelease(CherryPyAPI):
    """
    TransactionRelease model class for data release workflow.

    Attributes:
        +-------------------+-----------------------------------------------+
        | Name              | Description                                   |
        +===================+===============================================+
        | transaction       | transaction to be released                    |
        +-------------------+-----------------------------------------------+
        | authorized_person | authorized person originating the release     |
        +-------------------+-----------------------------------------------+
    """

    authorized_person = ForeignKeyField(
        Users, backref='authorized_releases')
    transaction = ForeignKeyField(
        Transactions, backref='release_state', primary_key=True)

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(TransactionRelease, self).to_hash(**flags)
        obj['transaction'] = int(self.__data__['transaction'])
        # pylint: disable=no-member
        obj['authorized_person'] = int(self.__data__['authorized_person'])
        # pylint: enable=no-member

        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(TransactionRelease, self).from_hash(obj)
        self._set_only_if('transaction', obj, 'transaction', lambda: Transactions.get(
            Transactions.id == obj['transaction']))
        self._set_only_if('authorized_person', obj, 'authorized_person', lambda: Users.get(
            Users.id == obj['authorized_person']))

    @classmethod
    def where_clause(cls, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(TransactionRelease, cls).where_clause(kwargs)
        return cls._where_attr_clause(where_clause, kwargs, ['authorized_person', 'transaction'])
