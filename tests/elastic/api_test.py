#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the ElasticAPI object for managing data in ES."""
from unittest import TestCase
from json import dumps, loads
import httpretty
from elasticsearch import TransportError
from pacifica.metadata.orm.utils import unicode_type
from pacifica.metadata.elastic.orm import ElasticAPI
from . import ES_CLUSTER_BODY


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
        response_body = {
            'took': 1,
            'errors': False,
            'items': [
                {
                    'index': {
                        '_index': 'pacifica',
                        '_type': 'ElasticAPI',
                        '_id': '127',
                        '_version': 1,
                        'result': 'created',
                        'forced_refresh': False,
                        'status': 201
                    }
                }
            ]
        }
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/_nodes/_all/http',
                               body=dumps(ES_CLUSTER_BODY),
                               content_type='application/json')
        httpretty.register_uri(httpretty.HEAD, url, status=404)
        httpretty.register_uri(httpretty.POST, 'http://127.0.0.1:9200/_bulk',
                               body=dumps(response_body),
                               content_type='application/json')
        ElasticAPI.elastic_upload([obj_hash])
        self.assertEqual(httpretty.last_request().method, 'POST')
        sent_body = httpretty.last_request().parsed_body
        self.assertTrue(isinstance(sent_body, unicode_type))
        sent_body = loads(sent_body.split('\n')[1])
        self.assertTrue('_id' not in sent_body)
        for key, value in sent_body.items():
            self.assertEqual(value, obj_hash[key])

    @httpretty.activate
    def test_failed_upload(self):
        """Test the upload class method failed upload."""
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/_nodes/_all/http',
                               body=dumps(ES_CLUSTER_BODY),
                               content_type='application/json')
        obj_hash = {
            '_id': 127,
            u'foo': u'bar'
        }
        url = 'http://127.0.0.1:9200/pacifica/ElasticAPI/127'
        httpretty.register_uri(httpretty.HEAD, url,
                               status=500)
        # pylint: disable=broad-except
        try:
            ElasticAPI.elastic_upload([obj_hash])
        except TransportError as ex:
            self.assertEqual(httpretty.last_request().method, 'HEAD')
            self.assertEqual(ex.__class__, TransportError)
            self.assertEqual(ex.status_code, 500)
        # pylint: enable=broad-except

    @httpretty.activate
    def test_delete(self):
        """Test the delete class method."""
        url = 'http://127.0.0.1:9200/pacifica/ElasticAPI/127'
        obj = ElasticAPI()
        # pylint: disable=invalid-name
        obj.id = 127
        # pylint: enable=invalid-name
        response_body = {
            'status': 'deleted!'
        }
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/_nodes/_all/http',
                               body=dumps(ES_CLUSTER_BODY),
                               content_type='application/json')
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
        # pylint: disable=invalid-name
        obj.id = 127
        # pylint: enable=invalid-name
        response_body = {
            'status': 'error!'
        }
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/_nodes/_all/http',
                               body=dumps(ES_CLUSTER_BODY),
                               content_type='application/json')
        httpretty.register_uri(httpretty.DELETE, url,
                               body=dumps(response_body),
                               content_type='application/json',
                               status=500)
        # pylint: disable=broad-except
        try:
            ElasticAPI.elastic_delete(obj)
        except TransportError as ex:
            self.assertEqual(httpretty.last_request().method, 'DELETE')
            self.assertEqual(ex.__class__, TransportError)
            self.assertEqual(ex.status_code, 500)
        # pylint: enable=broad-except

    @httpretty.activate
    def test_elastic_mapping(self):
        """Test the elastic_mapping class method."""
        url = 'http://127.0.0.1:9200/pacifica/_mapping/ElasticAPI'
        obj = ElasticAPI()
        # pylint: disable=invalid-name
        obj.id = 127
        # pylint: enable=invalid-name

        response_body = {
            'status': 'mapped!'
        }
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/_nodes/_all/http',
                               body=dumps(ES_CLUSTER_BODY),
                               content_type='application/json')
        httpretty.register_uri(httpretty.PUT, url,
                               body=dumps(response_body),
                               content_type='application/json')
        ElasticAPI.create_elastic_mapping()
        self.assertEqual(httpretty.last_request().method, 'PUT')

    @httpretty.activate
    def test_failed_elastic_mapping(self):
        """Test the elastic mapping class method failed upload."""
        url = 'http://127.0.0.1:9200/pacifica/_mapping/ElasticAPI'
        obj = ElasticAPI()
        # pylint: disable=invalid-name
        obj.id = 127
        # pylint: enable=invalid-name
        response_body = {
            'status': 'error!'
        }
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/_nodes/_all/http',
                               body=dumps(ES_CLUSTER_BODY),
                               content_type='application/json')
        httpretty.register_uri(httpretty.PUT, url,
                               body=dumps(response_body),
                               content_type='application/json',
                               status=500)
        # pylint: disable=broad-except
        try:
            ElasticAPI.create_elastic_mapping()
        except TransportError as ex:
            self.assertEqual(httpretty.last_request().method, 'PUT')
            self.assertEqual(ex.__class__, TransportError)
            self.assertEqual(ex.status_code, 500)
        # pylint: enable=broad-except
