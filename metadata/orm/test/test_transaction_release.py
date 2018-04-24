#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.transaction_release import TransactionRelease
from metadata.orm.test.test_transactions import SAMPLE_TRANSACTION_HASH
from metadata.orm.test.test_transactions import TestTransactions
from metadata.orm.transactions import Transactions
from metadata.orm.test.test_users import SAMPLE_USER_HASH as SAMPLE_CREATOR_HASH

SAMPLE_TRANS_RELEASE_HASH = {
    '_id': 1,
    'authorized_person': SAMPLE_CREATOR_HASH['_id'],
    'transaction': SAMPLE_TRANSACTION_HASH['_id']
}


class TestTransactionRelease(TestBase):
    """Test the Keywords ORM object."""

    obj_cls = TransactionRelease
    obj_id = TransactionRelease.id

    @classmethod
    def base_create_dep_objs(cls):
        """Build the object and make dependent user object."""
        trans = Transactions()
        TestTransactions.base_create_dep_objs()
        trans.from_hash(SAMPLE_TRANSACTION_HASH)
        trans.save(force_insert=True)

    def test_transrelease_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_TRANS_RELEASE_HASH)

    def test_transrelease_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_TRANS_RELEASE_HASH))

    def test_transrelease_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_TRANS_RELEASE_HASH)
