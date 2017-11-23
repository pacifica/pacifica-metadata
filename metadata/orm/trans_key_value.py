#!/usr/bin/python
"""TransactionKeyValue links Transactions and Keys and Values objects."""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.base import DB
from metadata.orm.utils import index_hash
from metadata.orm.transactions import Transactions
from metadata.orm.values import Values
from metadata.orm.keys import Keys
from metadata.rest.orm import CherryPyAPI


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

    transaction = ForeignKeyField(Transactions, related_name='metadata')
    key = ForeignKeyField(Keys, related_name='trans_links')
    value = ForeignKeyField(Values, related_name='trans_links')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('transaction', 'key', 'value')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(TransactionKeyValue, TransactionKeyValue).elastic_mapping_builder(obj)
        obj['transaction_id'] = obj['key_id'] = obj['value_id'] = \
            {'type': 'integer'}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(TransactionKeyValue, self).to_hash(**flags)
        obj['_id'] = index_hash(int(self.key.id),
                                int(self.transaction.id),
                                int(self.value.id))
        obj['transaction_id'] = int(self.transaction.id)
        obj['key_id'] = int(self.key.id)
        obj['value_id'] = int(self.value.id)
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(TransactionKeyValue, self).from_hash(obj)
        if 'transaction_id' in obj:
            self.transaction = Transactions.get(Transactions.id == obj['transaction_id'])
        if 'value_id' in obj:
            self.value = Values.get(Values.id == obj['value_id'])
        if 'key_id' in obj:
            self.key = Keys.get(Keys.id == obj['key_id'])

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(TransactionKeyValue, self).where_clause(kwargs)
        if 'transaction_id' in kwargs:
            trans = Transactions.get(Transactions.id == kwargs['transaction_id'])
            where_clause &= Expression(TransactionKeyValue.transaction, OP.EQ, trans)
        if 'key_id' in kwargs:
            key = Keys.get(Keys.id == kwargs['key_id'])
            where_clause &= Expression(TransactionKeyValue.key, OP.EQ, key)
        if 'value_id' in kwargs:
            value = Values.get(Values.id == kwargs['value_id'])
            where_clause &= Expression(TransactionKeyValue.value, OP.EQ, value)
        return where_clause
