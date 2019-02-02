#!/usr/bin/python
# -*- coding: utf-8 -*-
"""TransactionKeyValue links Transactions and Keys and Values objects."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.base import DB
from pacifica.metadata.orm.utils import index_hash
from pacifica.metadata.orm.transactions import Transactions
from pacifica.metadata.orm.values import Values
from pacifica.metadata.orm.keys import Keys
from pacifica.metadata.rest.orm import CherryPyAPI


class TransactionKeyValue(CherryPyAPI):
    """
    TransactionKeyValue attributes are foreign keys.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | transaction       | Link to the Transactions model      |
        +-------------------+-------------------------------------+
        | key               | Link to the Keys model              |
        +-------------------+-------------------------------------+
        | value             | Link to the Values model            |
        +-------------------+-------------------------------------+
    """

    transaction = ForeignKeyField(Transactions, backref='metadata')
    key = ForeignKeyField(Keys, backref='trans_links')
    value = ForeignKeyField(Values, backref='trans_links')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('transaction', 'key', 'value')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(TransactionKeyValue, self).to_hash(**flags)
        obj['_id'] = index_hash(int(self.__data__['key']),
                                int(self.__data__['transaction']),
                                int(self.__data__['value']))
        obj['transaction_id'] = int(self.__data__['transaction'])
        obj['key_id'] = int(self.__data__['key'])
        obj['value_id'] = int(self.__data__['value'])
        # obj['kv_pair'] = {'key': int(self.key_id), 'value': int(self.value_id)}
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(TransactionKeyValue, self).from_hash(obj)
        self._set_only_if(
            'transaction_id', obj, 'transaction',
            lambda: Transactions.get(Transactions.id == obj['transaction_id'])
        )
        self._set_only_if(
            'value_id', obj, 'value', lambda: Values.get(
                Values.id == obj['value_id'])
        )
        self._set_only_if(
            'key_id', obj, 'key', lambda: Keys.get(Keys.id == obj['key_id'])
        )

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(TransactionKeyValue, cls).where_clause(kwargs)
        attrs = ['transaction', 'key', 'value']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
