#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the analytical tools ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.analytical_tools import AnalyticalTools

SAMPLE_TOOL_HASH = {
    "_id": 127,
    "name": "proposal",
    "encoding": "UTF8"
}

SAMPLE_UNICODE_TOOL_HASH = {
    "_id": 127,
    "name": u"proposalé",
    "encoding": "UTF8"
}

class TestAnalyticalTools(TestBase):
    """
    Test the AnalyticalTools ORM object
    """
    obj_cls = AnalyticalTools
    obj_id = AnalyticalTools.id

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the AnalyticalTools object
        """
        return [AnalyticalTools]

    def test_tools_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_TOOL_HASH)

    def test_unicode_tools_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_UNICODE_TOOL_HASH)

    def test_tools_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_TOOL_HASH))

    def test_tools_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_TOOL_HASH)

    def test_unicode_tools_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_UNICODE_TOOL_HASH)

if __name__ == '__main__':
    main()
