#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the keys ORM object
"""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.values import Values

SAMPLE_VALUE_HASH = {
    "_id": 127,
    "value": "43278a",
    "encoding": "UTF8"
}

SAMPLE_UNICODE_VALUE_HASH = {
    "_id": 127,
    "value": u"43278é",
    "encoding": "UTF8"
}

class TestValues(TestBase):
    """
    Test the Values ORM object
    """
    obj_cls = Values
    obj_id = Values.id

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the Values object
        """
        return [Values]

    def test_values_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_VALUE_HASH)

    def test_unicode_values_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_UNICODE_VALUE_HASH)

    def test_values_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_VALUE_HASH))

    def test_values_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_VALUE_HASH)

    def test_unicode_values_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_UNICODE_VALUE_HASH)
