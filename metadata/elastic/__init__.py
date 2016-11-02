#!/usr/bin/python
"""Elastic search orm classes and utilities."""
from os import getenv
from time import sleep
import requests

ELASTIC_CONNECT_ATTEMPTS = 10
ELASTIC_WAIT = 1
DEFAULT_ELASTIC_ENDPOINT = getenv('ELASTICDB_PORT', 'tcp://127.0.0.1:9200').replace('tcp', 'http')
ELASTIC_ENDPOINT = getenv('ELASTIC_ENDPOINT', DEFAULT_ELASTIC_ENDPOINT)
ELASTIC_INDEX = 'pacifica'
ES_INDEX_URL = '{0}/{1}'.format(ELASTIC_ENDPOINT, ELASTIC_INDEX)
ES_STATUS_URL = '{0}/_stats'.format(ELASTIC_ENDPOINT)


def create_elastic_index():
    """Create the elastic search index for all our data."""
    ret = requests.get(ES_INDEX_URL.encode('utf-8'))
    if ret.status_code == 200:
        return
    ret = requests.put(ES_INDEX_URL.encode('utf-8'))
    if ret.status_code != 200:
        raise Exception('create_elastic_index: {0}\n'.format(ret.status_code))


def try_es_connect(attempts=0):
    """Recursively try to connect to elasticsearch."""
    try:
        ret = requests.get(ES_STATUS_URL.encode('utf-8'))
        if ret.status_code != 200:
            raise Exception('try_es_connect: {0}\n'.format(ret.status_code))
    # pylint: disable=broad-except
    except Exception as ex:
        # pylint: enable=broad-except
        if attempts < ELASTIC_CONNECT_ATTEMPTS:
            sleep(ELASTIC_WAIT)
            attempts += 1
            try_es_connect(attempts)
        else:
            raise ex
