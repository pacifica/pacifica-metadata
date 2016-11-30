#!/usr/bin/python
"""Test the ORM interface CherryPyAPI."""
from time import time
from json import loads, dumps
import requests
import cherrypy
from test_files.loadit import main
from metadata.rest.test import CPCommonTest
from metadata.orm.keys import Keys


class TestCherryPyAPI(CPCommonTest):
    """Test the CherryPyAPI class."""

    def test_methods(self):
        """Test the PUT (insert) method."""
        main()
        req = requests.get(
            '{0}/keys?page_number=1&items_per_page=1'.format(self.url))
        self.assertEqual(req.status_code, 200)
        keys = loads(req.content)
        self.assertEqual(len(keys), 1)
        set_hash = {'key': 'Break Keys', 'updated': None}
        req = requests.post('{0}/keys'.format(self.url),
                            data=dumps(set_hash), headers=self.headers)
        self.assertEqual(req.status_code, 200)
        req = requests.get('{0}/keys'.format(self.url))
        self.assertEqual(req.status_code, 200)
        keys = loads(req.content)
        self.assertEqual(len(keys), 2)
        for key in keys:
            self.assertEqual(key['key'], 'Break Keys')

        req = requests.get('{0}/keys'.format(self.url))
        self.assertEqual(req.status_code, 200)
        keys = loads(req.content)
        self.assertEqual(len(keys), 2)

        # update a foreign key to something that isn't there
        req = requests.post('{0}/file_key_value?file_id=103'.format(self.url),
                            data='{"key_id": 107}', headers=self.headers)
        self.assertEqual(req.status_code, 500)

        req = requests.put('{0}/file_key_value'.format(self.url),
                           data='{"key_id": 107, "file_id": 103, "value_id": 103}',
                           headers=self.headers)
        self.assertEqual(req.status_code, 500)

        # just try invalid json
        req = requests.post('{0}/keys'.format(self.url),
                            data='{ some bad json}', headers=self.headers)
        self.assertEqual(req.status_code, 500)
        req = requests.put('{0}/keys'.format(self.url),
                           data='{ some bad json}', headers=self.headers)
        self.assertEqual(req.status_code, 500)

        # insert one item
        req = requests.put('{0}/keys'.format(self.url),
                           data=dumps({'_id': 1, 'key': 'blarg'}), headers=self.headers)
        self.assertEqual(req.status_code, 200)

        # try to insert the same item again
        req = requests.put('{0}/keys'.format(self.url),
                           data=dumps({'_id': 1, 'key': 'blarg'}), headers=self.headers)
        self.assertEqual(req.status_code, 400)

        # delete the item I just put in
        req = requests.delete('{0}/keys?key=blarg'.format(self.url))
        self.assertEqual(req.status_code, 200)

    def test_perf_of_large_insert(self):
        """Create 10000 records of Values and try to insert them."""
        values = []
        for j in range(0, 10):
            values.append([])
            for i in range(0, 1000):
                values[j].append(
                    {'_id': 20000 + i + (j * 1000), 'value': 'Value {0}'.format(i + (j * 1000))})
        txt_dumps = []
        for trans in values:
            txt_dumps.append(dumps(trans))
        start_time = time()
        for txt_trans in txt_dumps:
            req = requests.put('{0}/values'.format(self.url),
                               data=txt_trans, headers=self.headers)
            self.assertEqual(req.status_code, 200)
        end_time = time()
        self.assertTrue(end_time - start_time < 45)

    def test_set_or_create(self):
        """Test the internal set or create method."""
        key = '{"_id": 4096, "key": "bigger"}'
        obj = Keys()
        # pylint: disable=protected-access
        obj._set_or_create(key)
        keys = '[{"_id": 4097, "key": "blah"}]'
        obj._set_or_create(keys)
        obj._set_or_create(key)
        hit_exception = False
        try:
            obj._set_or_create('{ bad json }')
        except cherrypy.HTTPError:
            hit_exception = True
        self.assertTrue(hit_exception)
        # pylint: enable=protected-access
