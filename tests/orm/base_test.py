#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Base testing module implements the temporary database to be used."""
from datetime import datetime
from unittest import TestCase
from json import dumps, loads
from pacifica.metadata.orm.base import PacificaModel
from pacifica.metadata.orm import ORM_OBJECTS
from pacifica.metadata.orm.utils import unicode_type
from pacifica.metadata.orm.globals import DB


class TestBase(TestCase):
    """Setup the test cases for the base object attributes for the ORM."""

    obj_cls = PacificaModel
    # pylint: disable=no-member
    obj_id = PacificaModel.id
    # pylint: enable=no-member

    @classmethod
    def setUpClass(cls):
        """Connect to the database."""
        if not DB.is_closed():  # pragma: no cover this is just in case
            DB.close()
        DB.connect()

    def setUp(self):
        """Setup the database."""
        self._models = self.dependent_cls()
        DB.create_tables(self._models)

    def tearDown(self):
        """Tear down the database."""
        DB.drop_tables(self._models)

    @classmethod
    def tearDownClass(cls):
        """Close the database connection."""
        DB.close()

    @staticmethod
    def dependent_cls():
        """Return dependent classes."""
        return ORM_OBJECTS

    @classmethod
    def base_create_dep_objs(cls):
        """Create dependent objects."""
        pass

    def base_create_obj(self, cls, obj_hash):
        """Create obj based on the class given."""
        self.base_create_dep_objs()
        obj = cls()
        if 'updated' not in obj_hash:
            change_date_chk = datetime.utcnow()
            obj.updated = change_date_chk
        obj.from_hash(obj_hash)
        obj.save(force_insert=True)
        if 'updated' not in obj_hash:
            self.assertEqual(obj.last_change_date(), unicode_type(
                change_date_chk.isoformat(' ')))
        return obj

    def base_test_hash(self, obj_hash):
        """
        Base hash test.

        create a new object out of the hash
        save the object to the DB
        pull the object out of the DB using the obj_id column
        create a new hash from the new object
        check all keys in the new hash from the obj_hash passed
        """
        obj = self.base_create_obj(self.obj_cls, obj_hash)
        # pylint: disable=no-member
        new_obj = self.obj_cls.get(
            self.obj_id == getattr(obj, self.obj_id.column_name))
        # pylint: enable=no-member
        chk_obj_hash = new_obj.to_hash()
        self.assertTrue('_id' in chk_obj_hash)
        for key in obj_hash.keys():
            self.assertEqual(chk_obj_hash[key], obj_hash[key])

    def base_test_json(self, json_str):
        """
        Base test json.

        pass the json string to the objects from_json method
        save the object to the DB
        get the new object using column in obj_id
        convert the object to json
        """
        self.assertEqual(type(json_str), str)
        self.base_create_dep_objs()
        if not isinstance(loads(json_str), dict):
            raise ValueError('json_str not dict')
        obj = self.obj_cls()
        obj.from_hash(loads(json_str))
        obj.save(force_insert=True)
        # pylint: disable=no-member
        new_obj = self.obj_cls.get(
            self.obj_id == getattr(obj, self.obj_id.column_name))
        # pylint: enable=no-member
        chk_obj_json = dumps(new_obj.to_hash())
        self.assertEqual(type(chk_obj_json), str)

    @staticmethod
    def base_where_clause_search(obj, kwargs):
        """Use kwargs as options to where clause to search for obj and return."""
        expr = obj.where_clause(kwargs)
        return obj.select().where(expr)

    def base_where_clause_search_expr(self, obj_hash, **kwargs):
        """Search for a objects on single search parameters."""
        obj = self.base_create_obj(self.obj_cls, obj_hash)
        chk_obj = self.base_where_clause_search(obj, kwargs)[0]
        chk_obj_hash = chk_obj.to_hash()
        for key in obj_hash.keys():
            self.assertEqual(
                chk_obj_hash[key], obj_hash[key],
                unicode_type('{} not equal to {}').format(chk_obj_hash[key], obj_hash[key])
            )

    def base_where_clause(self, obj_hash):
        """
        Base where clause checking.

        create a new object from the obj_hash
        save it to the database
        check all keys in obj_hash separately
        query a new object using that key and value in obj_hash
        compare the pulled object hash with obj_hash
        """
        obj = self.base_create_obj(self.obj_cls, obj_hash)
        for (key, val) in obj_hash.items():
            chk_obj = self.base_where_clause_search(obj, {key: val})[0]
            chk_obj_hash = chk_obj.to_hash()
            for chkkey in obj_hash.keys():
                self.assertEqual(
                    chk_obj_hash[chkkey], obj_hash[chkkey],
                    unicode_type('{} not equal to {}').format(chk_obj_hash[chkkey], obj_hash[chkkey])
                )
