#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.doidatasets import DOIDataSets

SAMPLE_DOIDATASET_HASH = {
    '_id': 142,
    'doi': 'halitosis',
    'name': 'halitosis',
    'encoding': 'UTF8'
}

# yes a DOI can be unicode....
# https://www.doi.org/doi_handbook/2_Numbering.html#2.2.1
SAMPLE_UNICODE_DOIDATASET_HASH = {
    '_id': 143,
    'doi': u'blargééééé',
    'name': u'blargééééé',
    'encoding': 'UTF8'
}


class TestDOIDataSets(TestBase):
    """Test the Keywords ORM object."""

    obj_cls = DOIDataSets
    obj_id = DOIDataSets.id

    def test_doidatasets_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_DOIDATASET_HASH)

    def test_unicode_doidatasets_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_UNICODE_DOIDATASET_HASH)

    def test_doidatasets_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_DOIDATASET_HASH))

    def test_doidatasets_search_expr(self):
        """Test the hash portion using base object method."""
        self.base_where_clause_search_expr(
            SAMPLE_UNICODE_DOIDATASET_HASH,
            keyword_operator='ILIKE',
            keyword=u'%é%'
        )

    def test_doidatasets_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_DOIDATASET_HASH)

    def test_unicode_doidatasets_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_UNICODE_DOIDATASET_HASH)
