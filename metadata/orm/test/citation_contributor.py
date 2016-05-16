#!/usr/bin/python
"""
Test the citation contributor ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.citation_contributor import CitationContributor
from metadata.orm.test.contributors import SAMPLE_CONTRIBUTOR_HASH, TestContributors
from metadata.orm.contributors import Contributors
from metadata.orm.test.citations import SAMPLE_CITATION_HASH, TestCitations
from metadata.orm.citations import Citations

SAMPLE_CITATION_CONTRIBUTOR_HASH = {
    "citation_id": SAMPLE_CITATION_HASH['_id'],
    "author_id": SAMPLE_CONTRIBUTOR_HASH['_id'],
    "author_precedence": 20
}

class TestCitationContributor(TestBase):
    """
    Test the Files ORM object
    """
    obj_cls = CitationContributor
    obj_id = CitationContributor.author

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the CitationContributor object
        """
        ret = [CitationContributor]
        ret += TestContributors.dependent_cls()
        ret += TestCitations.dependent_cls()
        return ret

    @classmethod
    def base_create_dep_objs(cls):
        """
        Create all objects that Files depend on.
        """
        cite1 = Citations()
        TestCitations.base_create_dep_objs()
        cite1.from_hash(SAMPLE_CITATION_HASH)
        cite1.save(force_insert=True)
        contrib = Contributors()
        TestContributors.base_create_dep_objs()
        contrib.from_hash(SAMPLE_CONTRIBUTOR_HASH)
        contrib.save(force_insert=True)

    def test_citation_contributor_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_CITATION_CONTRIBUTOR_HASH)

    def test_citation_contributor_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_CITATION_CONTRIBUTOR_HASH))

    def test_citation_contributor_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_CITATION_CONTRIBUTOR_HASH)

if __name__ == '__main__':
    main()
