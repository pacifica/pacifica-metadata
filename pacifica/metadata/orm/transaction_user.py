#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Contains the model for metadata transaction user."""
from peewee import ForeignKeyField
from pacifica.metadata.rest.orm import CherryPyAPI
from pacifica.metadata.orm.users import Users
from pacifica.metadata.orm.transactions import Transactions

# NOTE: change to transaction user


class TransactionUser(CherryPyAPI):
    """
    TransactionRelease model class for transaction user relationships.

    Attributes:
        +-------------------+-----------------------------------------------+
        | Name              | Description                                   |
        +===================+===============================================+
        | transaction       | transaction to be released                    |
        +-------------------+-----------------------------------------------+
        | user              | user reference                                |
        +-------------------+-----------------------------------------------+
    """

    # NOTE: add relationship field
    user = ForeignKeyField(Users, backref='transactions')
    transaction = ForeignKeyField(Transactions, backref='users', primary_key=True)

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(TransactionUser, self).to_hash(**flags)
        obj['transaction'] = int(self.__data__['transaction'])
        obj['user'] = int(self.__data__['user'])

        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(TransactionUser, self).from_hash(obj)
        self._set_only_if('transaction', obj, 'transaction', lambda: Transactions.get(
            Transactions.id == obj['transaction']))
        self._set_only_if('user', obj, 'user', lambda: Users.get(
            Users.id == obj['user']))

    @classmethod
    def where_clause(cls, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(TransactionUser, cls).where_clause(kwargs)
        return cls._where_attr_clause(where_clause, kwargs, ['user', 'transaction'])
