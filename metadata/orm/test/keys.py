#!/usr/bin/python
"""
Test the keys ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.keys import Keys

class TestKeys(TestBase):
    """
    Test the Keys ORM object
    """
    obj_cls = Keys
    obj_id = Keys.key_id
    sample_key = {
        "key_id": 127,
        "key": "proposal"
    }

    def test_keys_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(self.sample_key)

    def test_keys_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(self.sample_key))

    def test_keys_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(self.sample_key)


if __name__ == '__main__':
    main()
