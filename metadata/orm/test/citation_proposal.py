#!/usr/bin/python
"""
Test the file_key_values ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.citation_proposal import CitationProposal
from metadata.orm.test.proposals import SAMPLE_PROPOSAL_HASH
from metadata.orm.proposals import Proposals
from metadata.orm.test.citations import SAMPLE_CITATION_HASH
from metadata.orm.citations import Citations
from metadata.orm.test.journals import SAMPLE_JOURNAL_HASH
from metadata.orm.journals import Journals

SAMPLE_CITATION_PROPOSAL_HASH = {
    "proposal_id": SAMPLE_PROPOSAL_HASH['_id'],
    "citation_id": SAMPLE_CITATION_HASH['_id']
}

class TestCitationProposal(TestBase):
    """
    Test the InstitutionPerson ORM object
    """
    dependent_cls = [Journals, Citations, Proposals]
    obj_cls = CitationProposal
    obj_id = CitationProposal.proposal

    def base_create_dep_objs(self):
        """
        Create all objects that FileKeyValue need.
        """
        journal = Journals()
        journal.from_hash(SAMPLE_JOURNAL_HASH)
        journal.save(force_insert=True)
        prop = Proposals()
        prop.from_hash(SAMPLE_PROPOSAL_HASH)
        prop.save(force_insert=True)
        cite = Citations()
        cite.from_hash(SAMPLE_CITATION_HASH)
        cite.save(force_insert=True)

    def test_citation_proposal_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_CITATION_PROPOSAL_HASH)

    def test_citation_proposal_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_CITATION_PROPOSAL_HASH))

    def test_citation_proposal_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_CITATION_PROPOSAL_HASH)

if __name__ == '__main__':
    main()
