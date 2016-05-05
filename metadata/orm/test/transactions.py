#!/usr/bin/python
"""
Test the keys ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.transactions import Transactions
from metadata.orm.test.users import SAMPLE_USER_HASH
from metadata.orm.users import Users

SAMPLE_TRANSACTION_HASH = {
    "_id": 127,
    "verified": "True",
    "submitter": SAMPLE_USER_HASH['_id']
}

class TestTransactions(TestBase):
    """
    Test the Transactions ORM object
    """
    dependent_cls = [Users]
    obj_cls = Transactions
    obj_id = Transactions.id

    def base_create_dep_objs(self):
        """
        Build the object and make dependent user object.
        """
        user = Users()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)

    def test_transactions_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_TRANSACTION_HASH)

    def test_transactions_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_TRANSACTION_HASH))

    def test_transactions_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_TRANSACTION_HASH)

if __name__ == '__main__':
    main()
