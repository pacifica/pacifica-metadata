#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.citation_doi import CitationDOI
from metadata.orm.citations import Citations
from metadata.orm.test.test_citations import SAMPLE_CITATION_HASH
from metadata.orm.test.test_citations import TestCitations
from metadata.orm.doidatasets import DOIDataSets
from metadata.orm.test.test_doidatasets import SAMPLE_DOIDATASET_HASH
from metadata.orm.test.test_doidatasets import TestDOIDataSets

SAMPLE_CITATION_DOI_HASH = {
    'citation': SAMPLE_CITATION_HASH['_id'],
    'doi': SAMPLE_DOIDATASET_HASH['doi']
}


class TestCitationDOI(TestBase):
    """Test the Keywords ORM object."""

    obj_cls = CitationDOI
    obj_id = CitationDOI.citation

    @classmethod
    def base_create_dep_objs(cls):
        """Build the object and make dependent user object."""
        cite = Citations()
        TestCitations.base_create_dep_objs()
        cite.from_hash(SAMPLE_CITATION_HASH)
        cite.save(force_insert=True)
        doi_ds = DOIDataSets()
        TestDOIDataSets.base_create_dep_objs()
        doi_ds.from_hash(SAMPLE_DOIDATASET_HASH)
        doi_ds.save(force_insert=True)

    def test_citationdoi_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_CITATION_DOI_HASH)

    def test_citationdoi_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_CITATION_DOI_HASH))

    def test_citationdoi_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_CITATION_DOI_HASH)
