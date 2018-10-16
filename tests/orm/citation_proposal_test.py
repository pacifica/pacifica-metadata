#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from pacifica.metadata.orm.citation_proposal import CitationProposal
from pacifica.metadata.orm.proposals import Proposals
from pacifica.metadata.orm.citations import Citations
from .base_test import TestBase
from .proposals_test import SAMPLE_PROPOSAL_HASH, TestProposals
from .citations_test import SAMPLE_CITATION_HASH, TestCitations

SAMPLE_CITATION_PROPOSAL_HASH = {
    'proposal_id': SAMPLE_PROPOSAL_HASH['_id'],
    'citation_id': SAMPLE_CITATION_HASH['_id']
}


class TestCitationProposal(TestBase):
    """Test the InstitutionPerson ORM object."""

    obj_cls = CitationProposal
    obj_id = CitationProposal.proposal

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that FileKeyValue need."""
        prop1 = Proposals()
        TestProposals.base_create_dep_objs()
        prop1.from_hash(SAMPLE_PROPOSAL_HASH)
        prop1.save(force_insert=True)
        cite = Citations()
        TestCitations.base_create_dep_objs()
        cite.from_hash(SAMPLE_CITATION_HASH)
        cite.save(force_insert=True)

    def test_citation_proposal_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_CITATION_PROPOSAL_HASH)

    def test_citation_proposal_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_CITATION_PROPOSAL_HASH))

    def test_citation_proposal_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_CITATION_PROPOSAL_HASH)
