#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from pacifica.metadata.orm.test.base import TestBase
from pacifica.metadata.orm.doi_transaction import DOITransaction
from pacifica.metadata.orm.doidatasets import DOIDataSets
from pacifica.metadata.orm.test.test_doidatasets import SAMPLE_DOIDATASET_HASH
from pacifica.metadata.orm.test.test_doidatasets import TestDOIDataSets
from pacifica.metadata.orm.transaction_release import TransactionRelease
from pacifica.metadata.orm.test.test_transaction_release import SAMPLE_TRANS_RELEASE_HASH
from pacifica.metadata.orm.test.test_transaction_release import TestTransactionRelease

SAMPLE_DOI_RELEASE_HASH = {
    'doi': SAMPLE_DOIDATASET_HASH['doi'],
    'transaction': SAMPLE_TRANS_RELEASE_HASH['transaction']
}


class TestDOIRelease(TestBase):
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
        doi_ds = DOIDataSets()
        TestDOIDataSets.base_create_dep_objs()
        doi_ds.from_hash(SAMPLE_DOIDATASET_HASH)
        doi_ds.save(force_insert=True)

    def test_doirelease_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_DOI_RELEASE_HASH)

    def test_doirelease_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_DOI_RELEASE_HASH))

    def test_doirelease_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_DOI_RELEASE_HASH)
