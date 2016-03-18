#!/usr/bin/python
"""
Test the keys ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.users import Users

SAMPLE_USER_HASH = {
    "person_id": 127,
    "first_name": "John",
    "last_name": "Doe",
    "network_id": "guest"
}

class TestUsers(TestBase):
    """
    Test the Users ORM object
    """
    dependent_cls = []
    obj_cls = Users
    obj_id = Users.person_id

    def test_users_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_USER_HASH)

    def test_users_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_USER_HASH))

    def test_users_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_USER_HASH)

if __name__ == '__main__':
    main()
