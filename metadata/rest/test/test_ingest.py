#!/usr/bin/python
"""Test the ORM interface IngestAPI."""
from json import dumps
import requests
from cherrypy.test import helper
from test_files.loadit import main
from metadata.rest.test import CPCommonTest, DockerMetadata


class TestIngestAPI(CPCommonTest, helper.CPWebCase):
    """Test the CherryPyAPI class."""

    @classmethod
    def teardown_class(cls):
        """Tear down the services required by the server."""
        super(TestIngestAPI, cls).teardown_class()
        DockerMetadata.stop_services()

    def test_ingest_api(self):
        """Test the PUT (insert) method."""
        putdata = [
            {'destinationTable': 'Transactions._id', 'value': 1234},
            {'destinationTable': 'Transactions.submitter', 'value': 10},
            {'destinationTable': 'Transactions.proposal', 'value': '1234a'},
            {'destinationTable': 'Transactions.instrument', 'value': 54},
            {'destinationTable': 'TransactionKeyValue', 'key': 'Temp C', 'value': '27'},
            {'destinationTable': 'TransactionKeyValue', 'key': 'Temp F', 'value': '27'},
            {'destinationTable': 'TransactionKeyValue', 'key': 'Tag', 'value': 'foo'},
            {
                'destinationTable': 'Files',
                '_id': 34, 'name': 'foo.txt', 'subdir': 'a/b/',
                'ctime': 'Tue Nov 29 14:09:05 PST 2016',
                'mtime': 'Tue Nov 29 14:09:05 PST 2016',
                'size': 128, 'mimetype': 'text/plain'
            },
            {
                'destinationTable': 'FileKeyValue',
                'key': 'Micronic Adjustment',
                'value': '5.66%',
                'file_id': 34
            },

            {
                'destinationTable': 'Files',
                '_id': 35, 'name': 'bar.txt', 'subdir': 'a/b/',
                'ctime': 'Tue Nov 29 14:09:05 PST 2016',
                'mtime': 'Tue Nov 29 14:09:05 PST 2016',
                'size': 47, 'mimetype': 'text/plain'
            },
        ]
        main()
        req = requests.put(
            '{0}/ingest'.format(self.url), data=dumps(putdata), headers={'content-type': 'application/json'})
        self.assertEqual(req.text, '{"status": "success"}')
        self.assertEqual(req.status_code, 200)
