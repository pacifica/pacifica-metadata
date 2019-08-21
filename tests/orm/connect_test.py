#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the connection logic see that it works as expected."""
import os
from unittest import TestCase
from mock import patch
from peewee import OperationalError
from pacifica.metadata.orm.sync import DB, OrmSync


class TestConnections(TestCase):
    """Test connecting to databases make sure it works."""

    @patch.object(DB, 'connect')
    def test_db_connect_and_fail(self, test_patch):
        """Try to connect to a database and fail."""
        test_patch.side_effect = OperationalError('connection refused')
        os.environ['DATABASE_CONNECT_ATTEMPTS'] = '1'
        os.environ['DATABASE_CONNECT_WAIT'] = '1'
        hit_exception = False
        try:
            OrmSync.dbconn_blocking()
        except OperationalError:
            hit_exception = True
        self.assertTrue(hit_exception)
