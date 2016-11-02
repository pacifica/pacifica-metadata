#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the keys ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.users import Users

SAMPLE_USER_HASH = {
    '_id': 127,
    'first_name': 'John',
    'middle_initial': 'G',
    'last_name': 'Doe',
    'email_address': 'jdoe@example.com',
    'encoding': 'UTF8'
}

SAMPLE_UNICODE_USER_HASH = {
    '_id': 127,
    'first_name': u'Téd',
    'middle_initial': u'é',
    'last_name': u'Doé',
    'network_id': u'guést',
    'email_address': u'tdoé@example.com',
    'encoding': 'UTF8'
}


class TestUsers(TestBase):
    """Test the Users ORM object."""

    obj_cls = Users
    obj_id = Users.id

    @classmethod
    def dependent_cls(cls):
        """Return dependent classes for the Users object."""
        return [Users]

    def test_users_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_USER_HASH)

    def test_unicode_users_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_UNICODE_USER_HASH)

    def test_users_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_USER_HASH))

    def test_users_search_expr(self):
        """Test the hash portion using base object method."""
        self.base_where_clause_search_expr(
            SAMPLE_USER_HASH,
            first_name_operator='ILIKE',
            first_name='%John%'
        )
        self.base_where_clause_search_expr(
            SAMPLE_UNICODE_USER_HASH,
            first_name_operator='ILIKE',
            first_name='%Téd%'
        )

    def test_users_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_USER_HASH)

    def test_unicode_users_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_UNICODE_USER_HASH)
