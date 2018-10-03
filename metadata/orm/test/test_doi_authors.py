#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.doi_entries import DOIEntries
from metadata.orm.test.test_doi_entries import TestDOIEntries
from metadata.orm.test.test_doi_entries import SAMPLE_DOIENTRIES_HASH
from metadata.orm.test.test_users import SAMPLE_USER_HASH, SAMPLE_UNICODE_USER_HASH
from metadata.orm.doi_authors import DOIAuthors

SAMPLE_DOIAUTHORS_HASH = {
    'doi_id': 1234567,
    'author_order': 1,
    'last_name': SAMPLE_USER_HASH['last_name'],
    'first_name': SAMPLE_USER_HASH['first_name'],
    'email': SAMPLE_USER_HASH['email_address'],
    'affiliation': 'EMSL',
    'orcid': '1234-2345-3456-4567'
}

# yes a DOI can be unicode....
# https://www.doi.org/doi_handbook/2_Numbering.html#2.2.1
SAMPLE_UNICODE_DOIAUTHORS_HASH = {
    'doi_id': 1234567,
    'author_order': 1,
    'last_name': SAMPLE_UNICODE_USER_HASH['last_name'],
    'first_name': SAMPLE_UNICODE_USER_HASH['first_name'],
    'email': SAMPLE_UNICODE_USER_HASH['email_address'],
    'affiliation': 'EMSL',
    'orcid': '1234-2345-3456-4567'
}


class TestDOIAuthors(TestBase):
    """Test the DOIAuthors ORM object."""

    obj_cls = DOIAuthors
    obj_id = DOIAuthors.id

    @classmethod
    def base_create_dep_objs(cls):
        """Build the object ands make dependent DOI entry object."""
        doi = DOIEntries()
        TestDOIEntries.base_create_dep_objs()
        doi.from_hash(SAMPLE_DOIENTRIES_HASH)
        doi.save()

    def test_doiauthors_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_DOIAUTHORS_HASH)

    def test_unicode_doiauthors_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_UNICODE_DOIAUTHORS_HASH)

    def test_doiauthors_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_DOIAUTHORS_HASH))

    def test_doiauthors_search_expr(self):
        """Test the hash portion using base object method."""
        self.base_where_clause_search_expr(
            SAMPLE_UNICODE_DOIAUTHORS_HASH,
            keyword_operator='ILIKE',
            keyword=u'%é%'
        )

    def test_doiauthors_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_DOIAUTHORS_HASH)

    def test_unicode_doiauthors_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_UNICODE_DOIAUTHORS_HASH)
