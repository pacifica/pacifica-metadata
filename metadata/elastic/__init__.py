#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Elastic search orm classes and utilities."""
from os import getenv
from time import sleep
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ElasticsearchException

ELASTIC_CONNECT_ATTEMPTS = 40
ELASTIC_WAIT = 3
DEFAULT_ELASTIC_ENDPOINT = getenv(
    'ELASTICDB_PORT', 'tcp://127.0.0.1:9200').replace('tcp', 'http')
ELASTIC_ENDPOINT = getenv('ELASTIC_ENDPOINT', DEFAULT_ELASTIC_ENDPOINT)
ELASTIC_INDEX = getenv('ELASTIC_INDEX', 'pacifica')
ES_INDEX_URL = '{0}/{1}'.format(ELASTIC_ENDPOINT, ELASTIC_INDEX)
ES_CLIENT_ARGS = {
    'sniff_on_start': True,
    'sniff_on_connection_fail': True,
    'sniffer_timeout': 60,
    'timeout': 60
}


def create_elastic_index():
    """Create the elastic search index for all our data."""
    cli = Elasticsearch([ELASTIC_ENDPOINT], **ES_CLIENT_ARGS)
    # pylint: disable=unexpected-keyword-arg
    cli.indices.create(index=ELASTIC_INDEX, ignore=400)
    # pylint: enable=unexpected-keyword-arg


def try_es_connect(attempts=0):
    """Recursively try to connect to elasticsearch."""
    try:
        cli = Elasticsearch([ELASTIC_ENDPOINT])
        cli.info()
    except ElasticsearchException as ex:
        if attempts < ELASTIC_CONNECT_ATTEMPTS:
            sleep(ELASTIC_WAIT)
            attempts += 1
            try_es_connect(attempts)
        else:
            raise ex
