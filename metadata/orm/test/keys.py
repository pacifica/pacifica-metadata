#!/usr/bin/python
"""
Test the keys ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.keys import Keys

SAMPLE_KEY_HASH = {
    "key_id": 127,
    "key": "proposal"
}

class TestKeys(TestBase):
    """
    Test the Keys ORM object
    """
    obj_cls = Keys
    obj_id = Keys.key_id

    def test_keys_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_KEY_HASH)

    def test_keys_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_KEY_HASH))

    def test_keys_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_KEY_HASH)
