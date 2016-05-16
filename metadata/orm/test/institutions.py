#!/usr/bin/python
"""
Test the keys ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.institutions import Institutions

SAMPLE_INSTITUTION_HASH = {
    "_id": 127,
    "institution_name": "STFU",
    "association_cd": "UNK",
    "is_foreign": 1
}

class TestInstitutions(TestBase):
    """
    Test the Institutions ORM object
    """
    obj_cls = Institutions
    obj_id = Institutions.id

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the Institutions object
        """
        return [Institutions]

    def test_institutions_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_INSTITUTION_HASH)

    def test_institutions_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_INSTITUTION_HASH))

    def test_institutions_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_INSTITUTION_HASH)

if __name__ == '__main__':
    main()
