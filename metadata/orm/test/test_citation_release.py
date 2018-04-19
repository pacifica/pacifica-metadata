#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.citation_release import CitationRelease
from metadata.orm.test.test_transaction_release import SAMPLE_TRANSACTION_RELEASE_HASH, TestTransactionRelease
from metadata.orm.transaction_release import TransactionRelease
from metadata.orm.test.test_citations import SAMPLE_CITATION_HASH, TestCitations
from metadata.orm.citations import Citations

SAMPLE_CITATION_RELEASE_HASH = {
    'release_id': SAMPLE_TRANSACTION_RELEASE_HASH['_id'],
    'citation_id': SAMPLE_CITATION_HASH['_id']
}


class TestCitationRelease(TestBase):
    """Test the DOIRelease ORM object."""

    obj_cls = CitationRelease
    obj_id = CitationRelease.citation

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that TransactionKeyValue need."""
        release = TransactionRelease()
        doi = DOIDataSets()
        TestTransactionRelease.base_create_dep_objs()
        release.from_hash(SAMPLE_TRANSACTION_RELEASE_HASH)
        release.save(force_insert=True)
        TestCitations.base_create_dep_objs()
        citation.from_hash(SAMPLE_CITATION_HASH)
        citation.save(force_insert=True)

    def test_citation_release_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_CITATION_RELEASE_HASH)

    def test_citation_release_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_CITATION_RELEASE_HASH))

    def test_citation_release_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_CITATION_RELEASE_HASH)
