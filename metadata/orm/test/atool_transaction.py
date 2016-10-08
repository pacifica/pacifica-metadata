#!/usr/bin/python
"""
Test the atool_proposal ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.atool_transaction import AToolTransaction
from metadata.orm.test.transactions import SAMPLE_TRANSACTION_HASH, TestTransactions
from metadata.orm.transactions import Transactions
from metadata.orm.test.analytical_tools import SAMPLE_TOOL_HASH, TestAnalyticalTools
from metadata.orm.analytical_tools import AnalyticalTools

SAMPLE_TOOL_TRANS_HASH = {
    "transaction_id": SAMPLE_TRANSACTION_HASH['_id'],
    "analytical_tool_id": SAMPLE_TOOL_HASH['_id']
}

class TestAToolTransaction(TestBase):
    """
    Test the Keys ORM object
    """
    obj_cls = AToolTransaction
    obj_id = AToolTransaction.transaction

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the TransactionKeyValue object
        """
        ret = [AToolTransaction]
        ret += TestTransactions.dependent_cls()
        ret += TestAnalyticalTools.dependent_cls()
        return ret

    @classmethod
    def base_create_dep_objs(cls):
        """
        Create all objects that TransactionKeyValue need.
        """
        trans = Transactions()
        tool = AnalyticalTools()
        TestTransactions.base_create_dep_objs()
        trans.from_hash(SAMPLE_TRANSACTION_HASH)
        trans.save(force_insert=True)
        TestAnalyticalTools.base_create_dep_objs()
        tool.from_hash(SAMPLE_TOOL_HASH)
        tool.save(force_insert=True)

    def test_tool_trans_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_TOOL_TRANS_HASH)

    def test_tool_trans_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_TOOL_TRANS_HASH))

    def test_tool_trans_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_TOOL_TRANS_HASH)

if __name__ == '__main__':
    main()
