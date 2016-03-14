#!/usr/bin/python
"""
Base testing module implements the temporary database to be used.
"""
from datetime import datetime
from time import mktime
from unittest import TestCase, main
from tempfile import NamedTemporaryFile
from json import dumps
from peewee import SqliteDatabase
from metadata.orm.base import PacificaModel


class TestBase(TestCase):
    """
    Setup the test cases for the base object attributes for the ORM
    """
    obj_cls = PacificaModel
    # pylint: disable=no-member
    obj_id = PacificaModel.id
    # pylint: enable=no-member
    zero_obj_hash = {
        'created': 0,
        'updated': 0,
        'deleted': 0
    }
    now_obj_hash = {
        'created': int(mktime(datetime.now().timetuple())),
        'updated': int(mktime(datetime.now().timetuple())),
        'deleted': 0
    }
    bad_obj_hash = {
        'created': 'blarg',
        'updated': int(mktime(datetime.now().timetuple())),
        'deleted': 0
    }

    def setUp(self):
        """
        Stub in the temporary database and create the tables
        """
        self.db_filename = NamedTemporaryFile()
        # pylint: disable=no-member
        # pylint: disable=protected-access
        self.obj_cls._meta.database = SqliteDatabase(self.db_filename.name)
        # pylint: enable=no-member
        # pylint: enable=protected-access
        self.obj_cls.create_table()

    def test_bad_dates_from_hash(self):
        """
        Test method to check the hash against zero dates.
        """
        exception_str = "invalid literal for int() with base 10: 'blarg'"
        try:
            self.base_test_hash(self.bad_obj_hash)
        except ValueError, ex:
            self.assertEqual(str(ex), exception_str)

    def test_zero_dates_from_hash(self):
        """
        Test method to check the hash against zero dates.
        """
        self.base_test_hash(self.zero_obj_hash)

    def test_zero_dates_from_json(self):
        """
        Test method to check the json against zero dates.
        """
        self.base_test_json(dumps(self.zero_obj_hash))

    def test_zero_dates_from_where(self):
        """
        Test method to check the where clause against zero dates.
        """
        self.base_where_clause(self.zero_obj_hash)

    def test_now_dates_from_hash(self):
        """
        Test method to check the hash against now dates
        """
        self.base_test_hash(self.now_obj_hash)

    def test_now_dates_from_json(self):
        """
        Test method to check the json against now dates
        """
        self.base_test_json(dumps(self.now_obj_hash))

    def test_now_dates_from_where(self):
        """
        Test method to check the where clause against now dates
        """
        self.base_where_clause(self.now_obj_hash)

    def base_test_hash(self, obj_hash):
        """
        Base hash test

        create a new object out of the hash
        save the object to the DB
        pull the object out of the DB using the obj_id column
        create a new hash from the new object
        check all keys in the new hash from the obj_hash passed
        """
        obj = self.obj_cls()
        obj.from_hash(obj_hash)
        obj.save(force_insert=True)
        new_obj = self.obj_cls.get(self.obj_id == getattr(obj, self.obj_id.db_column))
        chk_obj_hash = new_obj.to_hash()
        for key in obj_hash.keys():
            self.assertEqual(chk_obj_hash[key], obj_hash[key])

    def base_test_json(self, json_str):
        """
        Base test json

        pass the json string to the objects from_json method
        save the object to the DB
        get the new object using column in obj_id
        convert the object to json
        """
        self.assertEqual(type(json_str), str)
        obj = self.obj_cls()
        obj.from_json(json_str)
        obj.save(force_insert=True)
        new_obj = self.obj_cls.get(self.obj_id == getattr(obj, self.obj_id.db_column))
        chk_obj_json = new_obj.to_json()
        self.assertEqual(type(chk_obj_json), str)

    def base_where_clause(self, obj_hash):
        """
        Base where clause checking

        create a new object from the obj_hash
        save it to the database
        check all keys in obj_hash separately
        query a new object using that key and value in obj_hash
        compare the pulled object hash with obj_hash
        """
        obj = self.obj_cls()
        obj.from_hash(obj_hash)
        obj.save(force_insert=True)
        for key in obj_hash.keys():
            expr = obj.where_clause({key: obj_hash[key]})
            new_obj = obj.get(expr)
            chk_obj_hash = new_obj.to_hash()
            for key in obj_hash.keys():
                self.assertEqual(chk_obj_hash[key], obj_hash[key])

if __name__ == '__main__':
    main()
