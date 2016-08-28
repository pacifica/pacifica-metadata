#!/usr/bin/python
"""
this module tests the metadata.elastic module bits...
"""
from unittest import TestCase
from json import dumps
import httpretty
from metadata.elastic import create_elastic_index, try_es_connect

class TestElasticUtils(TestCase):
    """
    This tests the utility functions in metadata.elastic
    """

    @httpretty.activate
    def test_existing_elastic_index(self):
        """
        Test the create elastic index
        """
        response_body = {
            "status": "created!"
        }
        httpretty.register_uri(httpretty.GET, "http://127.0.0.1:9200/pacifica",
                               body=dumps(response_body),
                               content_type="application/json")
        create_elastic_index()
        self.assertEqual(httpretty.last_request().method, "GET")

    @httpretty.activate
    def test_create_elastic_index(self):
        """
        Test the create elastic index
        """
        response_body = {}
        created_body = {
            "status": "Created!"
        }
        httpretty.register_uri(httpretty.GET, "http://127.0.0.1:9200/pacifica",
                               body=dumps(response_body),
                               content_type="application/json",
                               status=404)
        httpretty.register_uri(httpretty.PUT, "http://127.0.0.1:9200/pacifica",
                               body=dumps(created_body),
                               content_type="application/json")
        create_elastic_index()
        self.assertEqual(httpretty.last_request().method, "PUT")

    @httpretty.activate
    def test_error_elastic_index(self):
        """
        Test the create elastic index
        """
        response_body = {}
        created_body = {
            "status": "ERROR"
        }
        httpretty.register_uri(httpretty.GET, "http://127.0.0.1:9200/pacifica",
                               body=dumps(response_body),
                               content_type="application/json",
                               status=404)
        httpretty.register_uri(httpretty.PUT, "http://127.0.0.1:9200/pacifica",
                               body=dumps(created_body),
                               content_type="application/json",
                               status=500)
        #pylint: disable=broad-except
        try:
            create_elastic_index()
        except Exception, ex:
            self.assertEqual(httpretty.last_request().method, "PUT")
            self.assertEqual(str(ex), "create_elastic_index: 500\n")
        #pylint: enable=broad-except

    @httpretty.activate
    def test_elastic_connect(self):
        """
        Test the create elastic index
        """
        response_body = {}
        httpretty.register_uri(httpretty.GET, "http://127.0.0.1:9200/_stats",
                               body=dumps(response_body),
                               content_type="application/json")
        try_es_connect()
        self.assertEqual(httpretty.last_request().method, "GET")

    @httpretty.activate
    def test_error_es_connect(self):
        """
        Test the create elastic index
        """
        httpretty.register_uri(httpretty.GET, "http://127.0.0.1:9200/_stats",
                               body="Trying to connect",
                               status=404)
        #pylint: disable=broad-except
        try:
            try_es_connect()
        except Exception, ex:
            self.assertEqual(httpretty.last_request().method, "GET")
            self.assertEqual(str(ex), "try_es_connect: 404\n")
        #pylint: enable=broad-except
