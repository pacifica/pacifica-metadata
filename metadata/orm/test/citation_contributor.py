#!/usr/bin/python
"""
Test the citation contributor ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.citation_contributor import CitationContributor
from metadata.orm.test.contributors import SAMPLE_CONTRIBUTOR_HASH
from metadata.orm.contributors import Contributors
from metadata.orm.test.users import SAMPLE_USER_HASH
from metadata.orm.users import Users
from metadata.orm.test.citations import SAMPLE_CITATION_HASH
from metadata.orm.citations import Citations
from metadata.orm.test.journals import SAMPLE_JOURNAL_HASH
from metadata.orm.journals import Journals
from metadata.orm.test.institutions import SAMPLE_INSTITUTION_HASH
from metadata.orm.institutions import Institutions

SAMPLE_CITATION_CONTRIBUTOR_HASH = {
    "citation_id": SAMPLE_CITATION_HASH['_id'],
    "author_id": SAMPLE_CONTRIBUTOR_HASH['_id'],
    "author_precedence": 20
}

class TestCitationContributor(TestBase):
    """
    Test the Files ORM object
    """
    dependent_cls = [Institutions, Users, Contributors, Journals, Citations]
    obj_cls = CitationContributor
    obj_id = CitationContributor.author

    def base_create_dep_objs(self):
        """
        Create all objects that Files depend on.
        """
        user = Users()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)
        journal = Journals()
        journal.from_hash(SAMPLE_JOURNAL_HASH)
        journal.save(force_insert=True)
        inst = Institutions()
        inst.from_hash(SAMPLE_INSTITUTION_HASH)
        inst.save(force_insert=True)
        cite = Citations()
        cite.from_hash(SAMPLE_CITATION_HASH)
        cite.save(force_insert=True)
        contrib = Contributors()
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
