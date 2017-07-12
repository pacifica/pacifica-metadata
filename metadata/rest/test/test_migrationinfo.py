#!/usr/bin/python
"""Test the ORM interface MigrationInfo."""
import requests
from metadata.rest.test import CPCommonTest


class TestMigrationInfoAPI(CPCommonTest):
    """Test the MigrationInfoAPI class."""

    __test__ = True

    def test_migrationinfo_api(self):
        """Test the GET method."""
        header_list = {'Content-Type': 'application/json'}

        # test instrument lookup for migration assistance
        url = '{0}/migrate/instruments/'
        req = requests.get(url=url, headers=header_list)
        self.assertEqual(req.status_code, 200)

        # test user lookup for migration assistance
        url = '{0}/migrate/users/'
        req = requests.get(url=url, headers=header_list)
        self.assertEqual(req.status_code, 200)

        url = '{0}/migrate/proposals/'
        req = requests.get(url=url, headers=header_list)
        self.assertEqual(req.status_code, 200)
