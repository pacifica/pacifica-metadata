#!/usr/bin/python
"""
Test the ORM interface CherryPyAPI
"""
from unittest import TestCase
from json import loads, dumps
from peewee import SqliteDatabase
from playhouse.test_utils import test_database
import httpretty
from cherrypy import HTTPError
from metadata.orm.keys import Keys
from metadata.orm.test.keys import SAMPLE_KEY_HASH

class TestCherryPyAPI(TestCase):
    """
    Test the CherryPyAPI class
    """

    def test_update_invalid_json(self):
        """
        Test _update with invalid json
        """
        test_obj = Keys()
        with test_database(SqliteDatabase(':memory:'), [Keys]):
            hit_exception = False
            test_obj.from_hash(SAMPLE_KEY_HASH)
            test_obj.save(force_insert=True)
            try:
                invalid_json = 'foo'
                # pylint: disable=protected-access
                test_obj._update(invalid_json, id=SAMPLE_KEY_HASH['_id'])
                # pylint: enable=protected-access
            except HTTPError, ex:
                hit_exception = True
                self.assertEqual(ex.code, 500)
                self.assertEqual(ex.args[1], 'No JSON object could be decoded')
            self.assertTrue(hit_exception)

    @httpretty.activate
    def test_update(self):
        """
        test the select method of CherryPyAPI
        """
        test_obj = Keys()
        url = "http://127.0.0.1:9200/pacifica/Keys/%s"%(SAMPLE_KEY_HASH['_id'])
        response_body = {
            "status": "uploaded Keys!"
        }
        httpretty.register_uri(httpretty.HEAD, url, status=200)
        httpretty.register_uri(httpretty.POST, '%s/_update'%(url),
                               body=dumps(response_body),
                               content_type="application/json")
        with test_database(SqliteDatabase(':memory:'), [Keys]):
            test_obj.from_hash(SAMPLE_KEY_HASH)
            test_obj.save(force_insert=True)
            test_update = SAMPLE_KEY_HASH
            test_update['key'] = 'foo'
            # pylint: disable=protected-access
            test_obj._update(dumps(test_update), id=SAMPLE_KEY_HASH['_id'])
            # pylint: enable=protected-access
            self.assertEqual(httpretty.last_request().method, "POST")

    def test_select(self):
        """
        test the select method of CherryPyAPI
        """
        test_obj = Keys()
        with test_database(SqliteDatabase(':memory:'), [Keys]):
            test_obj.from_hash(SAMPLE_KEY_HASH)
            test_obj.save(force_insert=True)
            # pylint: disable=protected-access
            data = loads(test_obj._select(id=SAMPLE_KEY_HASH['_id']))
            # pylint: enable=protected-access
            self.assertEqual(len(data), 1)
            for key, value in SAMPLE_KEY_HASH.iteritems():
                self.assertEqual(data[0][key], value)
