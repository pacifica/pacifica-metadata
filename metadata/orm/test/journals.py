#!/usr/bin/python
"""
Test the journals ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.journals import Journals

SAMPLE_JOURNAL_HASH = {
    "_id": 45,
    "journal_name": "Northern Yukon Master Workworking",
    "impact_factor": 10.0,
    "website_url": "http://www.ehwoodworkers.ca"
}

class TestJournals(TestBase):
    """
    Test the Journals ORM object
    """
    obj_cls = Journals
    obj_id = Journals.id

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the Journals object
        """
        return [Journals]

    def test_journal_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_JOURNAL_HASH)

    def test_journal_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_JOURNAL_HASH))

    def test_journal_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_JOURNAL_HASH)

if __name__ == '__main__':
    main()
