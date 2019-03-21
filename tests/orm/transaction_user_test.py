#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from pacifica.metadata.orm.transaction_user import TransactionUser
from pacifica.metadata.orm.transactions import Transactions
from pacifica.metadata.orm.users import Users
from .base_test import TestBase
from .transactions_test import SAMPLE_TRANSACTION_HASH, TestTransactions
from .users_test import SAMPLE_USER_HASH as SAMPLE_CREATOR_HASH
from .users_test import TestUsers

SAMPLE_TRANS_USER_HASH = {
    'user': SAMPLE_CREATOR_HASH['_id'],
    'transaction': SAMPLE_TRANSACTION_HASH['_id']
}


class TestTransactionUser(TestBase):
    """Test the Keywords ORM object."""

    obj_cls = TransactionUser
    obj_id = TransactionUser.transaction

    @classmethod
    def base_create_dep_objs(cls):
        """Build the object and make dependent user object."""
        user3 = Users()
        TestUsers.base_create_dep_objs()
        user3.from_hash(SAMPLE_CREATOR_HASH)
        user3.save(force_insert=True)
        rel_trans = Transactions()
        TestTransactions.base_create_dep_objs()
        rel_trans.from_hash(SAMPLE_TRANSACTION_HASH)
        rel_trans.save(force_insert=True)

    def test_transuser_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_TRANS_USER_HASH)

    def test_transuser_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_TRANS_USER_HASH))

    def test_transuser_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_TRANS_USER_HASH)
