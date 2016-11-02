#!/usr/bin/python
"""Test the ElasticAPI object for managing data in ES."""
from unittest import TestCase
from json import dumps, loads
import httpretty
from metadata.orm.utils import unicode_type
from metadata.elastic.orm import ElasticAPI


class TestElasticAPI(TestCase):
    """Test the elasic API class methods."""

    @httpretty.activate
    def test_upload(self):
        """Test the upload class method."""
        obj_hash = {
            '_id': 127,
            u'foo': u'bar'
        }
        url = 'http://127.0.0.1:9200/pacifica/ElasticAPI/127'
        obj = ElasticAPI()
        obj.id = 127
        setattr(obj, 'to_hash', lambda: obj_hash)
        response_body = {
            'status': 'uploaded!'
        }
        httpretty.register_uri(httpretty.HEAD, url, status=404)
        httpretty.register_uri(httpretty.PUT, '{0}/_create'.format(url),
                               body=dumps(response_body),
                               content_type='application/json')
        ElasticAPI.elastic_upload(obj)
        self.assertEqual(httpretty.last_request().method, 'PUT')
        sent_body = httpretty.last_request().parsed_body
        self.assertTrue(isinstance(sent_body, unicode_type))
        sent_body = loads(sent_body)
        self.assertTrue('_id' not in sent_body)
        for key, value in sent_body.iteritems():
            self.assertEqual(value, obj_hash[key])

    @httpretty.activate
    def test_failed_upload(self):
        """Test the upload class method failed upload."""
        obj_hash = {
            '_id': 127,
            u'foo': u'bar'
        }
        url = 'http://127.0.0.1:9200/pacifica/ElasticAPI/127'
        obj = ElasticAPI()
        obj.id = 127
        setattr(obj, 'to_hash', lambda: obj_hash)
        httpretty.register_uri(httpretty.HEAD, url,
                               status=500)
        # pylint: disable=broad-except
        try:
            ElasticAPI.elastic_upload(obj)
        except Exception as ex:
            self.assertEqual(httpretty.last_request().method, 'HEAD')
            self.assertEqual(str(ex), 'TransportError(500, u\'\')')
        # pylint: enable=broad-except

    @httpretty.activate
    def test_delete(self):
        """Test the delete class method."""
        url = 'http://127.0.0.1:9200/pacifica/ElasticAPI/127'
        obj = ElasticAPI()
        obj.id = 127
        response_body = {
            'status': 'deleted!'
        }
        httpretty.register_uri(httpretty.DELETE, url,
                               body=dumps(response_body),
                               content_type='application/json')
        ElasticAPI.elastic_delete(obj)
        self.assertEqual(httpretty.last_request().method, 'DELETE')

    @httpretty.activate
    def test_failed_delete(self):
        """Test the delete class method failed upload."""
        url = 'http://127.0.0.1:9200/pacifica/ElasticAPI/127'
        obj = ElasticAPI()
        obj.id = 127
        response_body = {
            'status': 'error!'
        }
        httpretty.register_uri(httpretty.DELETE, url,
                               body=dumps(response_body),
                               content_type='application/json',
                               status=500)
        # pylint: disable=broad-except
        try:
            ElasticAPI.elastic_delete(obj)
        except Exception as ex:
            self.assertEqual(httpretty.last_request().method, 'DELETE')
            self.assertEqual(str(ex), 'TransportError(500, u\'{0}\')'.format(dumps(response_body)))
        # pylint: enable=broad-except

    @httpretty.activate
    def test_elastic_mapping(self):
        """Test the elastic_mapping class method."""
        url = 'http://127.0.0.1:9200/_mapping/ElasticAPI'
        obj = ElasticAPI()
        obj.id = 127
        response_body = {
            'status': 'mapped!'
        }
        httpretty.register_uri(httpretty.PUT, url,
                               body=dumps(response_body),
                               content_type='application/json')
        ElasticAPI.create_elastic_mapping()
        self.assertEqual(httpretty.last_request().method, 'PUT')

    @httpretty.activate
    def test_failed_elastic_mapping(self):
        """Test the elastic mapping class method failed upload."""
        url = 'http://127.0.0.1:9200/_mapping/ElasticAPI'
        obj = ElasticAPI()
        obj.id = 127
        response_body = {
            'status': 'error!'
        }
        httpretty.register_uri(httpretty.PUT, url,
                               body=dumps(response_body),
                               content_type='application/json',
                               status=500)
        # pylint: disable=broad-except
        try:
            ElasticAPI.create_elastic_mapping()
        except Exception as ex:
            self.assertEqual(httpretty.last_request().method, 'PUT')
            self.assertEqual(str(ex), 'TransportError(500, u\'{0}\')'.format(dumps(response_body)))
        # pylint: enable=broad-except
