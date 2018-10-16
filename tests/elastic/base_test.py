#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module tests the metadata.elastic module bits."""
from unittest import TestCase
from json import dumps
import httpretty
from elasticsearch import TransportError
from pacifica.metadata.elastic import create_elastic_index, try_es_connect
from . import ES_CLUSTER_BODY


class TestElasticUtils(TestCase):
    """This tests the utility functions in metadata.elastic."""

    @httpretty.activate
    def test_existing_elastic_index(self):
        """Test the create elastic index."""
        response_body = {
            'status': 'created!'
        }
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/_nodes/_all/http',
                               body=dumps(ES_CLUSTER_BODY),
                               content_type='application/json')
        httpretty.register_uri(httpretty.PUT, 'http://127.0.0.1:9200/pacifica',
                               body=dumps(response_body),
                               content_type='application/json')
        create_elastic_index()
        self.assertEqual(httpretty.last_request().method, 'PUT')

    @httpretty.activate
    def test_create_elastic_index(self):
        """Test the create elastic index."""
        response_body = {}
        created_body = {
            'status': 'Created!'
        }
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/_nodes/_all/http',
                               body=dumps(ES_CLUSTER_BODY),
                               content_type='application/json')
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/pacifica',
                               body=dumps(response_body),
                               content_type='application/json', status=404)
        httpretty.register_uri(httpretty.PUT, 'http://127.0.0.1:9200/pacifica',
                               body=dumps(created_body),
                               content_type='application/json')
        create_elastic_index()
        self.assertEqual(httpretty.last_request().method, 'PUT')

    @httpretty.activate
    def test_error_elastic_index(self):
        """Test the create elastic index."""
        hit_exception = False
        response_body = {}
        created_body = {
            'status': 'ERROR'
        }
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/_nodes/_all/http',
                               body=dumps(ES_CLUSTER_BODY),
                               content_type='application/json')
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/pacifica',
                               body=dumps(response_body),
                               content_type='application/json',
                               status=404)
        httpretty.register_uri(httpretty.PUT, 'http://127.0.0.1:9200/pacifica',
                               body=dumps(created_body),
                               content_type='application/json',
                               status=500)
        # pylint: disable=broad-except
        try:
            create_elastic_index()
        except TransportError as ex:
            hit_exception = True
            self.assertEqual(httpretty.last_request().method, 'PUT')
            self.assertEqual(ex.__class__, TransportError)
            self.assertEqual(ex.status_code, 500)
        # pylint: enable=broad-except
        self.assertTrue(hit_exception)

    @httpretty.activate
    def test_elastic_connect(self):
        """Test the create elastic index."""
        response_body = {}
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/_nodes/_all/http',
                               body=dumps(ES_CLUSTER_BODY),
                               content_type='application/json')
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/',
                               body=dumps(response_body),
                               content_type='application/json')
        try_es_connect()
        self.assertEqual(httpretty.last_request().method, 'GET')

    @httpretty.activate
    def test_error_es_connect(self):
        """Test the create elastic index."""
        hit_exception = False
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/_nodes/_all/http',
                               body='Trying to connect',
                               status=404)
        httpretty.register_uri(httpretty.GET, 'http://127.0.0.1:9200/',
                               body='Trying to connect',
                               status=404)
        # pylint: disable=broad-except
        try:
            try_es_connect(30)
        except Exception as ex:
            hit_exception = True
            self.assertEqual(httpretty.last_request().method, 'GET')
            self.assertTrue('Trying to connect' in str(ex))
        # pylint: enable=broad-except
        self.assertTrue(hit_exception)
