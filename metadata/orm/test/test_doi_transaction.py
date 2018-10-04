#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.doi_transaction import DOITransaction
from metadata.orm.doi_entries import DOIEntries
from metadata.orm.test.test_doi_entries import SAMPLE_DOIENTRIES_HASH
from metadata.orm.transaction_release import TransactionRelease
from metadata.orm.test.test_transaction_release import SAMPLE_TRANS_RELEASE_HASH
from metadata.orm.test.test_transaction_release import TestTransactionRelease

SAMPLE_DOI_RELEASE_HASH = {
    'doi': SAMPLE_DOIENTRIES_HASH['doi'],
    'transaction': SAMPLE_TRANS_RELEASE_HASH['transaction']
}


class TestDOITransaction(TestBase):
    """Test the Keywords ORM object."""

    obj_cls = DOITransaction
    obj_id = DOITransaction.doi

    @classmethod
    def base_create_dep_objs(cls):
        """Build the object and make dependent user object."""
        trans_rel = TransactionRelease()
        TestTransactionRelease.base_create_dep_objs()
        trans_rel.from_hash(SAMPLE_TRANS_RELEASE_HASH)
        trans_rel.save(force_insert=True)

        doi_ds = DOIEntries()
        doi_ds.from_hash(SAMPLE_DOIENTRIES_HASH)
        doi_ds.save(force_insert=True)

    def test_doitransaction_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_DOI_RELEASE_HASH)

    def test_doitransaction_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_DOI_RELEASE_HASH))

    def test_doitransaction_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_DOI_RELEASE_HASH)
