#!/usr/bin/python
"""
Base testing module implements the temporary database to be used.
"""
from datetime import datetime
from time import mktime
from json import dumps
from unittest import main
from metadata.orm.base import PacificaModel
from metadata.orm.test.base import TestBase

SAMPLE_ZERO_HASH = {
    'created': 0,
    'updated': 0,
    'deleted': 0
}
SAMPLE_REP_HASH = {
    'created': int(mktime(datetime.now().timetuple())),
    'updated': int(mktime(datetime.now().timetuple())),
    'deleted': 0
}
SAMPLE_BAD_HASH = {
    'created': 'blarg',
    'updated': int(mktime(datetime.now().timetuple())),
    'deleted': 0
}

class TestDBDates(TestBase):
    """
    Setup the test cases for the base object attributes for the ORM
    """
    dependent_cls = []
    obj_cls = PacificaModel
    # pylint: disable=no-member
    obj_id = PacificaModel.id
    # pylint: enable=no-member

    def test_bad_dates_from_hash(self):
        """
        Test method to check the hash against zero dates.
        """
        exception_str = "invalid literal for int() with base 10: 'blarg'"
        try:
            self.base_test_hash(SAMPLE_BAD_HASH)
        except ValueError, ex:
            self.assertEqual(str(ex), exception_str)

    def test_zero_dates_from_hash(self):
        """
        Test method to check the hash against zero dates.
        """
        self.base_test_hash(SAMPLE_ZERO_HASH)

    def test_zero_dates_from_json(self):
        """
        Test method to check the json against zero dates.
        """
        self.base_test_json(dumps(SAMPLE_ZERO_HASH))

    def test_zero_dates_from_where(self):
        """
        Test method to check the where clause against zero dates.
        """
        self.base_where_clause(SAMPLE_ZERO_HASH)

    def test_now_dates_from_hash(self):
        """
        Test method to check the hash against now dates
        """
        self.base_test_hash(SAMPLE_REP_HASH)

    def test_now_dates_from_json(self):
        """
        Test method to check the json against now dates
        """
        self.base_test_json(dumps(SAMPLE_REP_HASH))

    def test_now_dates_from_where(self):
        """
        Test method to check the where clause against now dates
        """
        self.base_where_clause(SAMPLE_REP_HASH)

if __name__ == '__main__':
    main()
