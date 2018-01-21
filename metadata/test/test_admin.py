#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the admin tools methods."""
import os
from argparse import Namespace
from unittest import TestCase
from mock import patch
from peewee import SqliteDatabase
from playhouse.test_utils import test_database
import metadata.orm as metaorm
from metadata.admin_cmd import main, essync, escreate


class TestAdminTool(TestCase):
    """Test the admin tool cli."""

    @patch('metadata.admin_cmd.essync')
    def test_main(self, test_patch):
        """Test the main method."""
        test_patch.return_value = 'Return a test thing'
        main('essync')
        self.assertTrue(test_patch.called)

    def test_es_commands(self):
        """Test the essync sub command."""
        os.environ['ELASTIC_INDEX'] = 'test_pacifica_index'
        args = Namespace()
        setattr(args, 'skip_mappings', False)
        setattr(args, 'threads', 8)
        with test_database(SqliteDatabase(':memory:'), metaorm.ORM_OBJECTS):
            metaorm.DB = SqliteDatabase(':memory:')
            escreate(args)
            essync(args)
        # pylint: disable=no-member
        self.assertEqual(args.threads, 8)
        # pylint: enable=no-member
