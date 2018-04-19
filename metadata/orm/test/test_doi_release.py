#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.doi_release import DOIRelease
from metadata.orm.test.test_transaction_release import SAMPLE_TRANSACTION_RELEASE_HASH, TestTransactionRelease
from metadata.orm.transaction_release import TransactionRelease
from metadata.orm.test.test_doidatasets import SAMPLE_DOIDATASET_HASH, TestDOIDataSets
from metadata.orm.doidatasets import DOIDataSets

SAMPLE_DOI_RELEASE_HASH = {
    'release_id': SAMPLE_TRANSACTION_RELEASE_HASH['_id'],
    'doi': SAMPLE_DOIDATASET_HASH['doi']
}


class TestDOIRelease(TestBase):
    """Test the DOIRelease ORM object."""

    obj_cls = DOIRelease
    obj_id = DOIRelease.doi

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that TransactionKeyValue need."""
        release = TransactionRelease()
        doi = DOIDataSets()
        TestTransactionRelease.base_create_dep_objs()
        release.from_hash(SAMPLE_TRANSACTION_RELEASE_HASH)
        release.save(force_insert=True)
        TestDOIDataSets.base_create_dep_objs()
        doi.from_hash(SAMPLE_DOIDATASET_HASH)
        doi.save(force_insert=True)

    def test_doi_release_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_DOI_RELEASE_HASH)

    def test_doi_release_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_DOI_RELEASE_HASH))

    def test_doi_release_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_DOI_RELEASE_HASH)
