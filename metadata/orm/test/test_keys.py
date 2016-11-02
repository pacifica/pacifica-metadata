#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the keys ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.keys import Keys

SAMPLE_KEY_HASH = {
    '_id': 127,
    'key': 'proposal',
    'encoding': 'UTF8'
}

SAMPLE_UNICODE_KEY_HASH = {
    '_id': 127,
    'key': u'proposalé',
    'encoding': 'UTF8'
}


class TestKeys(TestBase):
    """Test the Keys ORM object."""

    obj_cls = Keys
    obj_id = Keys.id

    @classmethod
    def dependent_cls(cls):
        """Return dependent classes for the Keys object."""
        return [Keys]

    def test_keys_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_KEY_HASH)

    def test_unicode_keys_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_UNICODE_KEY_HASH)

    def test_keys_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_KEY_HASH))

    def test_key_search_expr(self):
        """Test the hash portion using base object method."""
        self.base_where_clause_search_expr(
            SAMPLE_UNICODE_KEY_HASH,
            key_operator='ILIKE',
            key=u'%é%'
        )

    def test_keys_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_KEY_HASH)

    def test_unicode_keys_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_UNICODE_KEY_HASH)
