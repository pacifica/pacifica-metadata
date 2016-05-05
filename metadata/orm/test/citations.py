#!/usr/bin/python
"""
Test the citations ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.citations import Citations
from metadata.orm.journals import Journals
from metadata.orm.test.journals import SAMPLE_JOURNAL_HASH

SAMPLE_CITATION_HASH = {
    "_id": 43,
    "article_title": "Applications of Dove-Tail Joints in Log Cabin Constructions",
    "journal_id": SAMPLE_JOURNAL_HASH['_id'],
    "journal_volume": 43,
    "journal_issue": 42,
    "page_range": "34-45",
    "abstract_text": """
This is a very long abstract about the unique applications of Dove-
Tail joints during a recent construction of a wonderful log cabin in
northern Yukon.
""",
    "xml_text": """<?xml version="1.0" encoding="UTF-8" ?>
<article>
  <abstract>blah blah blah</abstract>
</article>
""",
    "release_authorization_id": "Released",
    "doi_reference": "doi:10.1037/rmh0000008"
}

class TestCitations(TestBase):
    """
    Test the Citations ORM object
    """
    dependent_cls = [Journals]
    obj_cls = Citations
    obj_id = Citations.id

    def base_create_dep_objs(self):
        """
        Create all objects that Files depend on.
        """
        journal = Journals()
        journal.from_hash(SAMPLE_JOURNAL_HASH)
        journal.save(force_insert=True)

    def test_citations_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_CITATION_HASH)

    def test_citations_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_CITATION_HASH))

    def test_citations_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_CITATION_HASH)

if __name__ == '__main__':
    main()
