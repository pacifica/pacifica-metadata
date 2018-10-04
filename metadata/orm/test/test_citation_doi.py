#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.citation_doi import CitationDOI
from metadata.orm.citations import Citations
from metadata.orm.test.test_citations import SAMPLE_CITATION_HASH
from metadata.orm.test.test_citations import TestCitations
from metadata.orm.doi_entries import DOIEntries
from metadata.orm.test.test_doi_entries import SAMPLE_DOIENTRIES_HASH
from metadata.orm.test.test_doi_entries import TestDOIEntries

SAMPLE_CITATION_DOI_HASH = {
    'citation': SAMPLE_CITATION_HASH['_id'],
    'doi': SAMPLE_DOIENTRIES_HASH['doi']
}


class TestCitationDOI(TestBase):
    """Test the Keywords ORM object."""

    obj_cls = CitationDOI
    obj_id = CitationDOI.citation

    @classmethod
    def base_create_dep_objs(cls):
        """Build the object and make dependent user object."""
        doi = DOIEntries()
        TestDOIEntries.base_create_dep_objs()
        doi.from_hash(SAMPLE_DOIENTRIES_HASH)
        doi.save(force_insert=True)

        cite = Citations()
        TestCitations.base_create_dep_objs()
        cite.from_hash(SAMPLE_CITATION_HASH)
        cite.save(force_insert=True)

    def test_citationdoi_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_CITATION_DOI_HASH)

    def test_citationdoi_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_CITATION_DOI_HASH))

    def test_citationdoi_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_CITATION_DOI_HASH)
