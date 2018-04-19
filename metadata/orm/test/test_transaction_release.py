#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the keys ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.transaction_release import TransactionRelease
from metadata.orm.transactions import Transactions
from metadata.orm.test.test_transactions import TestTransactions
from metadata.orm.test.test_transactions import SAMPLE_TRANSACTION_HASH
from metadata.orm.test.test_users import SAMPLE_USER_HASH as SAMPLE_PERSON_HASH
from metadata.orm.test.test_users import TestUsers
from metadata.orm.users import Users

SAMPLE_TRANSACTION_RELEASE_HASH = {
    '_id': 1,
    'transaction': SAMPLE_TRANSACTION_HASH['_id'],
    'release_state': 1,
    'person': SAMPLE_PERSON_HASH['_id']
}


class TestTransactionRelease(TestBase):
    """Test the TransactionRelease ORM object."""

    obj_cls = TransactionRelease
    obj_id = TransactionRelease.id

    @classmethod
    def base_create_dep_objs(cls):
        """Build the object and make dependent user object."""
        person = Users()
        TestUsers.base_create_dep_objs()
        person.from_hash(SAMPLE_PERSON_HASH)
        person.save(force_insert=True)
        transaction = Transactions()
        TestTransactions.base_create_dep_objs()
        transaction.from_hash(SAMPLE_TRANSACTION_HASH)
        transaction.save(force_insert=True)

    def test_transaction_release_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_TRANSACTION_RELEASE_HASH)

    def test_transaction_release_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_TRANSACTION_RELEASE_HASH))

    def test_transaction_release_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_TRANSACTION_RELEASE_HASH)
