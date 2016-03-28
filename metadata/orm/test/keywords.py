#!/usr/bin/python
"""
Test the file_key_values ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.keywords import Keywords
from metadata.orm.test.citations import SAMPLE_CITATION_HASH
from metadata.orm.citations import Citations
from metadata.orm.test.journals import SAMPLE_JOURNAL_HASH
from metadata.orm.journals import Journals

SAMPLE_KEYWORD_HASH = {
    "keyword_id": 142,
    "citation_id": SAMPLE_CITATION_HASH['citation_id'],
    "keyword": "halitosis"
}

class TestKeywords(TestBase):
    """
    Test the InstitutionPerson ORM object
    """
    dependent_cls = [Journals, Citations]
    obj_cls = Keywords
    obj_id = Keywords.keyword_id

    def base_create_dep_objs(self):
        """
        Create all objects that FileKeyValue need.
        """
        journal = Journals()
        journal.from_hash(SAMPLE_JOURNAL_HASH)
        journal.save(force_insert=True)
        cite = Citations()
        cite.from_hash(SAMPLE_CITATION_HASH)
        cite.save(force_insert=True)

    def test_keywords_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_KEYWORD_HASH)

    def test_keywords_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_KEYWORD_HASH))

    def test_keywords_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_KEYWORD_HASH)

if __name__ == '__main__':
    main()
