#!/usr/bin/python
"""
Test the groups ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.groups import Groups

SAMPLE_GROUP_HASH = {
    "_id": 10,
    "group_name": "Custodians",
    "is_admin": True
}

class TestGroups(TestBase):
    """
    Test the Groups ORM object
    """
    dependent_cls = []
    obj_cls = Groups
    obj_id = Groups.id

    def test_group_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_GROUP_HASH)

    def test_group_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_GROUP_HASH))

    def test_group_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_GROUP_HASH)

if __name__ == '__main__':
    main()
