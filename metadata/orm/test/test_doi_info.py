#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.doi_entries import DOIEntries
from metadata.orm.test.test_doi_entries import TestDOIEntries
from metadata.orm.test.test_doi_entries import SAMPLE_DOIENTRIES_HASH as SAMPLE_DOI_HASH
from metadata.orm.test.test_doi_entries import SAMPLE_UNICODE_DOIENTRIES_HASH as SAMPLE_UNICODE_DOI_HASH
from metadata.orm.doi_info import DOIInfo


SAMPLE_DOIINFO_HASH = {
    'doi': SAMPLE_DOI_HASH['doi'],
    'key': u'title',
    'value': u'My Super Title'
}

# yes a DOI can be unicode....
# https://www.doi.org/doi_handbook/2_Numbering.html#2.2.1
SAMPLE_UNICODE_DOIINFO_HASH = {
    'doi': SAMPLE_UNICODE_DOI_HASH['doi'],
    'key': u'töitle',
    'value': u'Meine Süpër Töitle'
}


class TestDOIInfo(TestBase):
    """Test the DOIAuthors ORM object."""

    obj_cls = DOIInfo
    obj_id = DOIInfo.doi

    @classmethod
    def base_create_dep_objs(cls):
        """Build the object ands make dependent DOI entry object."""
        uni_doi = DOIEntries()
        TestDOIEntries.base_create_dep_objs()
        uni_doi.from_hash(SAMPLE_UNICODE_DOI_HASH)
        uni_doi.save(force_insert=True)

        doi = DOIEntries()
        doi.from_hash(SAMPLE_DOI_HASH)
        doi.save(force_insert=True)

    def test_doiinfo_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_DOIINFO_HASH)

    def test_unicode_doiinfo_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_UNICODE_DOIINFO_HASH)

    def test_doiinfo_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_DOIINFO_HASH))

    def test_doiinfo_search_expr(self):
        """Test the hash portion using base object method."""
        self.base_where_clause_search_expr(
            SAMPLE_UNICODE_DOIINFO_HASH,
            keyword_operator='ILIKE',
            keyword=u'%ü%'
        )

    def test_doiinfo_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_DOIINFO_HASH)

    def test_unicode_doiinfo_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_UNICODE_DOIINFO_HASH)
