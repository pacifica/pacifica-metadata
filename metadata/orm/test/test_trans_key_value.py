#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the trans_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.trans_key_value import TransactionKeyValue
from metadata.orm.test.test_transactions import SAMPLE_TRANSACTION_HASH, TestTransactions
from metadata.orm.transactions import Transactions
from metadata.orm.test.test_keys import SAMPLE_KEY_HASH, TestKeys
from metadata.orm.keys import Keys
from metadata.orm.test.test_values import SAMPLE_VALUE_HASH, TestValues
from metadata.orm.values import Values

SAMPLE_TRANSACTION_KEY_VALUE_HASH = {
    'transaction_id': SAMPLE_TRANSACTION_HASH['_id'],
    'key_id': SAMPLE_KEY_HASH['_id'],
    'value_id': SAMPLE_VALUE_HASH['_id']
}


class TestTransactionKeyValue(TestBase):
    """Test the Keys ORM object."""

    obj_cls = TransactionKeyValue
    obj_id = TransactionKeyValue.transaction

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that TransactionKeyValue need."""
        trans = Transactions()
        keys = Keys()
        values = Values()
        TestTransactions.base_create_dep_objs()
        trans.from_hash(SAMPLE_TRANSACTION_HASH)
        trans.save(force_insert=True)
        TestKeys.base_create_dep_objs()
        keys.from_hash(SAMPLE_KEY_HASH)
        keys.save(force_insert=True)
        TestValues.base_create_dep_objs()
        values.from_hash(SAMPLE_VALUE_HASH)
        values.save(force_insert=True)

    def test_trans_key_value_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_TRANSACTION_KEY_VALUE_HASH)

    def test_trans_key_value_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_TRANSACTION_KEY_VALUE_HASH))

    def test_trans_key_value_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_TRANSACTION_KEY_VALUE_HASH)
