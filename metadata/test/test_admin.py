#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the admin tools methods."""
from argparse import Namespace
from unittest import TestCase
from mock import patch
from peewee import SqliteDatabase
from playhouse.test_utils import test_database
from metadata.orm import ORM_OBJECTS
from metadata.orm.keys import Keys
from metadata.admin_cmd import main, essync, escreate, render_obj, create_obj, objstr_to_ormobj, objstr_to_whereclause


class TestAdminTool(TestCase):
    """Test the admin tool cli."""

    def test_objstr_to_ormobj(self):
        """Test the string object to ORM object type check."""
        cls = objstr_to_ormobj('Keys')
        self.assertEqual(cls, Keys)
        hit_exception = False
        try:
            objstr_to_ormobj('Blah!')
        except ValueError:
            hit_exception = True
        self.assertTrue(hit_exception)

    def test_objstr_to_whereclause(self):
        """Test the string object to ORM where clause parsing."""
        where_clause = objstr_to_whereclause('{"_id": 1234}')
        self.assertTrue(isinstance(where_clause, dict))
        hit_exception = False
        try:
            objstr_to_whereclause('[]')
        except ValueError:
            hit_exception = True
        self.assertTrue(hit_exception)

    @patch('metadata.admin_cmd.essync')
    def test_main(self, test_patch):
        """Test the main method."""
        test_patch.return_value = 'Return a test thing'
        main('essync')
        self.assertTrue(test_patch.called)

    @patch('metadata.orm.try_db_connect')
    def test_es_commands(self, test_patch):
        """Test the essync sub command."""
        test_patch.return_value = True
        skip_args = Namespace()
        reg_args = Namespace()
        setattr(skip_args, 'skip_mappings', True)
        setattr(reg_args, 'skip_mappings', False)
        setattr(skip_args, 'threads', 8)
        setattr(reg_args, 'threads', 8)
        setattr(reg_args, 'items_per_page', 1)
        setattr(reg_args, 'objects', [Keys])
        with test_database(SqliteDatabase(':memory:'), ORM_OBJECTS):
            test_obj = Keys()
            test_obj.key = 'test_key'
            test_obj.save()
            escreate(skip_args)
            escreate(reg_args)
            essync(reg_args)
        self.assertTrue(test_patch.called)

    @patch('metadata.orm.try_db_connect')
    def test_render(self, test_patch):
        """Test render an object."""
        test_patch.return_value = True
        args = Namespace()
        setattr(args, 'object', Keys)
        setattr(args, 'where_clause', {'key': 'test_key'})
        setattr(args, 'recursion', 1)
        with test_database(SqliteDatabase(':memory:'), ORM_OBJECTS):
            test_obj = Keys()
            test_obj.key = 'test_key'
            test_obj.save()
            render_obj(args)
        self.assertTrue(test_patch.called)

    @patch('metadata.orm.try_db_connect')
    def test_create(self, test_patch):
        """Test the create obj."""
        test_patch.return_value = True
        args = Namespace()
        setattr(args, 'object', Keys)
        with test_database(SqliteDatabase(':memory:'), ORM_OBJECTS, create_tables=False):
            create_obj(args)
        self.assertTrue(test_patch.called)
