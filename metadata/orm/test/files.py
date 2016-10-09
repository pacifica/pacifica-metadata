#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the files ORM object
"""
from datetime import datetime
from time import mktime
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.files import Files
from metadata.orm.transactions import Transactions
from metadata.orm.test.transactions import SAMPLE_TRANSACTION_HASH, TestTransactions

SAMPLE_FILE_HASH = {
    "_id": 127,
    "name": "test.txt",
    "subdir": "a/b",
    "mimetype": "text/plain",
    "mtime": int(mktime(datetime.now().timetuple())),
    "ctime": int(mktime(datetime.now().timetuple())),
    "size": 1234,
    "transaction_id": SAMPLE_TRANSACTION_HASH['_id'],
    "encoding": "UTF8"
}

SAMPLE_UNICODE_FILE_HASH = {
    "_id": 127,
    "name": u'abcdé.txt',
    "subdir": u'abcdé/b',
    "mimetype": "text/plain",
    "mtime": int(mktime(datetime.now().timetuple())),
    "ctime": int(mktime(datetime.now().timetuple())),
    "size": 1234,
    "transaction_id": SAMPLE_TRANSACTION_HASH['_id'],
    "encoding": "UTF8"
}

class TestFiles(TestBase):
    """
    Test the Files ORM object
    """
    obj_cls = Files
    obj_id = Files.id

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the Files object
        """
        return TestTransactions.dependent_cls() + [Files]

    @classmethod
    def base_create_dep_objs(cls):
        """
        Create all objects that Files depend on.
        """
        trans = Transactions()
        TestTransactions.base_create_dep_objs()
        trans.from_hash(SAMPLE_TRANSACTION_HASH)
        trans.save(force_insert=True)

    def test_unicode_files_hash(self):
        """
        Test the unicode hash using base object method.
        """
        self.base_test_hash(SAMPLE_UNICODE_FILE_HASH)

    def test_files_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_FILE_HASH)

    def test_files_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_FILE_HASH))

    def test_files_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_FILE_HASH)

    def test_unicode_files_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_UNICODE_FILE_HASH)
