#!/usr/bin/python
"""
Base testing module implements the temporary database to be used.
"""
from unittest import TestCase, main
from peewee import SqliteDatabase
from playhouse.test_utils import test_database
from metadata.orm.base import PacificaModel

class TestBase(TestCase):
    """
    Setup the test cases for the base object attributes for the ORM
    """
    obj_cls = PacificaModel
    #pylint: disable=no-member
    obj_id = PacificaModel.id
    #pylint: enable=no-member

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes
        """
        return []

    @classmethod
    def base_create_dep_objs(cls):
        """
        Create dependent objects
        """
        pass

    def base_create_obj(self, cls, obj_hash):
        """
        Create obj based on the class given.
        """
        self.base_create_dep_objs()
        obj = cls()
        obj.from_hash(obj_hash)
        obj.save(force_insert=True)
        return obj

    def base_test_hash(self, obj_hash):
        """
        Base hash test

        create a new object out of the hash
        save the object to the DB
        pull the object out of the DB using the obj_id column
        create a new hash from the new object
        check all keys in the new hash from the obj_hash passed
        """
        with test_database(SqliteDatabase(':memory:'), self.dependent_cls()):
            obj = self.base_create_obj(self.obj_cls, obj_hash)
            new_obj = self.obj_cls.get(self.obj_id == getattr(obj, self.obj_id.db_column))
            chk_obj_hash = new_obj.to_hash()
            self.assertEqual('_id' in chk_obj_hash, True)
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
        with test_database(SqliteDatabase(':memory:'), self.dependent_cls()):
            self.assertEqual(type(json_str), str)
            self.base_create_dep_objs()
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
        with test_database(SqliteDatabase(':memory:'), self.dependent_cls()):
            obj = self.base_create_obj(self.obj_cls, obj_hash)
            for key in obj_hash.keys():
                expr = obj.where_clause({key: obj_hash[key]})
                new_obj = obj.get(expr)
                chk_obj_hash = new_obj.to_hash()
                for key in obj_hash.keys():
                    self.assertEqual(chk_obj_hash[key], obj_hash[key])

if __name__ == '__main__':
    main()
