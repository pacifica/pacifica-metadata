#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.doidatasets import DOIDataSets
from metadata.orm.test.test_users import SAMPLE_USER_HASH as SAMPLE_CREATOR_HASH
from metadata.orm.test.test_users import TestUsers
from metadata.orm.users import Users

SAMPLE_DOIDATASET_HASH = {
    '_id': 142,
    'doi': 'halitosis',
    'name': 'halitosis',
    'encoding': 'UTF8',
    'creator': SAMPLE_CREATOR_HASH['_id']
}

# yes a DOI can be unicode....
# https://www.doi.org/doi_handbook/2_Numbering.html#2.2.1
SAMPLE_UNICODE_DOIDATASET_HASH = {
    '_id': 143,
    'doi': u'blargééééé',
    'name': u'blargééééé',
    'encoding': 'UTF8',
    'creator': SAMPLE_CREATOR_HASH['_id']
}


class TestDOIDataSets(TestBase):
    """Test the Keywords ORM object."""

    obj_cls = DOIDataSets
    obj_id = DOIDataSets.id

    @classmethod
    def base_create_dep_objs(cls):
        """Build the object and make dependent user object."""
        submitter = Users()
        TestUsers.base_create_dep_objs()
        submitter.from_hash(SAMPLE_CREATOR_HASH)
        submitter.save(force_insert=True)

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
