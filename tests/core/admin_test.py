#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the admin tools methods."""
from argparse import Namespace
from datetime import timedelta
from unittest import TestCase
from mock import patch
from peewee import SqliteDatabase, DoesNotExist
import pacifica.metadata.orm as metaorm
from pacifica.metadata.admin_cmd import main, essync, escreate, render_obj, create_obj
from pacifica.metadata.admin_cmd import objstr_to_ormobj, objstr_to_whereclause, objstr_to_timedelta


class TestAdminTool(TestCase):
    """Test the admin tool cli."""

    def setUp(self):
        """Setup the database with in memory sqlite."""
        metaorm.DB = SqliteDatabase(':memory:')
        metaorm.create_elastic_index()
        for model in metaorm.ORM_OBJECTS:
            model.bind(metaorm.DB, bind_refs=False, bind_backrefs=False)
            model.create_elastic_mapping()
        metaorm.DB.connect()
        metaorm.DB.create_tables(metaorm.ORM_OBJECTS)

    def tearDown(self):
        """Tear down the database."""
        metaorm.DB.drop_tables(metaorm.ORM_OBJECTS)
        metaorm.DB.close()
        metaorm.DB = None

    def test_objstr_to_timedelta(self):
        """Test the string object to timedelta object."""
        ten_minutes = objstr_to_timedelta('10 minutes ago')
        self.assertEqual(ten_minutes, timedelta(minutes=10))

    def test_objstr_to_ormobj(self):
        """Test the string object to ORM object type check."""
        cls = objstr_to_ormobj('Keys')
        self.assertEqual(cls, metaorm.Keys)
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

    @patch('pacifica.metadata.admin_cmd.essync')
    def test_main(self, test_patch):
        """Test the main method."""
        test_patch.return_value = 'Return a test thing'
        main('essync')
        self.assertTrue(test_patch.called)

    @patch('pacifica.metadata.orm.try_db_connect')
    def test_render(self, test_patch):
        """Test render an object."""
        test_patch.return_value = True
        args = Namespace()
        setattr(args, 'object', metaorm.Keys)
        setattr(args, 'where_clause', {'key': 'test_key'})
        setattr(args, 'recursion', 1)
        setattr(args, 'delete', True)
        test_obj = metaorm.Keys()
        test_obj.key = 'test_key'
        test_obj.save()
        test_obj.elastic_upload([test_obj.to_hash()])
        render_obj(args)
        hit_exception = False
        try:
            metaorm.Keys().get()
        except DoesNotExist:
            hit_exception = True
        self.assertTrue(hit_exception)
        self.assertTrue(test_patch.called)

    @patch('pacifica.metadata.orm.try_db_connect')
    def test_create(self, test_patch):
        """Test the create obj."""
        test_patch.return_value = True
        args = Namespace()
        setattr(args, 'object', metaorm.Keys)
        create_obj(args)
        self.assertTrue(test_patch.called)


class TestAdminToolNoTables(TestCase):
    """Test the admin tool cli."""

    def setUp(self):
        """Setup the database with in memory sqlite."""
        metaorm.DB = SqliteDatabase('file:cachedb?mode=memory&cache=shared')
        for model in metaorm.ORM_OBJECTS:
            model.bind(metaorm.DB, bind_refs=False, bind_backrefs=False)
        metaorm.DB.connect()

    def tearDown(self):
        """Tear down the database."""
        metaorm.DB.drop_tables(metaorm.ORM_OBJECTS)
        metaorm.DB.close()
        metaorm.DB = None

    @patch('pacifica.metadata.orm.try_db_connect')
    def test_create_no_tables(self, test_patch):
        """Test the create obj."""
        test_patch.return_value = True
        args = Namespace()
        setattr(args, 'object', metaorm.Keys)
        create_obj(args)
        self.assertTrue(test_patch.called)


class TestAdminToolThreaded(TestCase):
    """Test the admin tool cli."""

    def setUp(self):
        """Setup the database with in memory sqlite."""
        metaorm.DB = SqliteDatabase('file:cachedb?mode=memory&cache=shared')
        for model in metaorm.ORM_OBJECTS:
            model.bind(metaorm.DB, bind_refs=False, bind_backrefs=False)
        metaorm.DB.connect()
        metaorm.DB.create_tables(metaorm.ORM_OBJECTS)

    def tearDown(self):
        """Tear down the database."""
        metaorm.DB.drop_tables(metaorm.ORM_OBJECTS)
        metaorm.DB.close()
        metaorm.DB = None

    @patch('pacifica.metadata.orm.try_db_connect')
    def test_es_commands(self, test_patch):
        """Test the essync sub command."""
        test_patch.return_value = True
        skip_args = Namespace()
        reg_args = Namespace()
        setattr(skip_args, 'skip_mappings', True)
        setattr(reg_args, 'skip_mappings', False)
        setattr(skip_args, 'threads', 1)
        setattr(reg_args, 'threads', 1)
        setattr(reg_args, 'items_per_page', 1)
        setattr(reg_args, 'time_ago', timedelta(days=100))
        setattr(reg_args, 'objects', [metaorm.Keys])
        test_obj = metaorm.Keys()
        test_obj.key = 'test_key'
        test_obj.save()
        escreate(skip_args)
        escreate(reg_args)
        essync(reg_args)
        self.assertTrue(test_patch.called)
