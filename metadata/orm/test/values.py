#!/usr/bin/python
"""
Test the keys ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.values import Values

SAMPLE_VALUE_HASH = {
    "value_id": 127,
    "value": "43278a"
}

class TestValues(TestBase):
    """
    Test the Values ORM object
    """
    dependent_cls = []
    obj_cls = Values
    obj_id = Values.value_id

    def test_values_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_VALUE_HASH)

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

if __name__ == '__main__':
    main()
