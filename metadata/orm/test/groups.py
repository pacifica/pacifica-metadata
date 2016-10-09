#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the groups ORM object
"""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.groups import Groups

SAMPLE_GROUP_HASH = {
    "_id": 10,
    "group_name": "Custodians",
    "is_admin": True,
    "encoding": "UTF8"
}

SAMPLE_UNICODE_GROUP_HASH = {
    "_id": 11,
    "group_name": u"Bléh",
    "is_admin": False,
    "encoding": "UTF8"
}

class TestGroups(TestBase):
    """
    Test the Groups ORM object
    """
    obj_cls = Groups
    obj_id = Groups.id

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the Groups object
        """
        return [Groups]

    def test_group_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_GROUP_HASH)

    def test_unicode_group_hash(self):
        """
        Test the unicode hash using base object method.
        """
        self.base_test_hash(SAMPLE_UNICODE_GROUP_HASH)

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

    def test_unicode_group_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_UNICODE_GROUP_HASH)
