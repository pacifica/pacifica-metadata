#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.doiresource import DOIResource
from metadata.orm.test.test_transactions import SAMPLE_TRANSACTION_HASH, TestTransactions
from metadata.orm.transactions import Transactions
from metadata.orm.test.test_doidatasets import SAMPLE_DOIDATASET_HASH, TestDOIDataSets
from metadata.orm.doidatasets import DOIDataSets

SAMPLE_DOIRESOURCE_HASH = {
    'transaction_id': SAMPLE_TRANSACTION_HASH['_id'],
    'key_id': SAMPLE_DOIDATASET_HASH['doi']
}


class TestDOIResource(TestBase):
    """Test the DOIResource ORM object."""

    obj_cls = DOIResource
    obj_id = DOIResource.transaction

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that TransactionKeyValue need."""
        trans = Transactions()
        doi = DOIDataSets()
        TestTransactions.base_create_dep_objs()
        trans.from_hash(SAMPLE_TRANSACTION_HASH)
        trans.save(force_insert=True)
        TestDOIDataSets.base_create_dep_objs()
        doi.from_hash(SAMPLE_DOIDATASET_HASH)
        doi.save(force_insert=True)

    def test_doiresource_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_DOIRESOURCE_HASH)

    def test_doiresource_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_DOIRESOURCE_HASH))

    def test_doiresource_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_DOIRESOURCE_HASH)
