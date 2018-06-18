#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.citation_transaction import CitationTransaction
from metadata.orm.citations import Citations
from metadata.orm.test.test_citations import SAMPLE_CITATION_HASH
from metadata.orm.test.test_citations import TestCitations
from metadata.orm.transaction_release import TransactionRelease
from metadata.orm.test.test_transaction_release import SAMPLE_TRANS_RELEASE_HASH
from metadata.orm.test.test_transaction_release import TestTransactionRelease

SAMPLE_CITATION_RELEASE_HASH = {
    'citation': SAMPLE_CITATION_HASH['_id'],
    'transaction': SAMPLE_TRANS_RELEASE_HASH['transaction']
}


class TestCitationRelease(TestBase):
    """Test the Keywords ORM object."""

    obj_cls = CitationTransaction
    obj_id = CitationTransaction.citation

    @classmethod
    def base_create_dep_objs(cls):
        """Build the object and make dependent user object."""
        cite = Citations()
        TestCitations.base_create_dep_objs()
        cite.from_hash(SAMPLE_CITATION_HASH)
        cite.save(force_insert=True)
        trans_rel = TransactionRelease()
        TestTransactionRelease.base_create_dep_objs()
        trans_rel.from_hash(SAMPLE_TRANS_RELEASE_HASH)
        trans_rel.save(force_insert=True)

    def test_citationrelease_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_CITATION_RELEASE_HASH)

    def test_citationrelease_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_CITATION_RELEASE_HASH))

    def test_citationrelease_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_CITATION_RELEASE_HASH)
