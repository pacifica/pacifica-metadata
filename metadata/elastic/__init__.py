#!/usr/bin/python
"""
Elastic search orm classes and utilities.
"""
from os import getenv
from time import sleep
from pycurl import Curl, URL, PUT, HTTP_CODE, error

ELASTIC_CONNECT_ATTEMPTS = 10
ELASTIC_WAIT = 1
DEFAULT_ELASTIC_ENDPOINT = getenv('ELASTICDB_PORT', 'tcp://127.0.0.1:9200').replace('tcp', 'http')
ELASTIC_ENDPOINT = getenv('ELASTIC_ENDPOINT', DEFAULT_ELASTIC_ENDPOINT)
ELASTIC_INDEX = 'pacifica'
ES_INDEX_URL = "%s/%s"%(ELASTIC_ENDPOINT, ELASTIC_INDEX)
ES_STATUS_URL = "%s/_stats"%(ELASTIC_ENDPOINT)

def create_elastic_index():
    """
    Create the elastic search index for all our data
    """
    try:
        curl = Curl()
        curl.setopt(URL, ES_INDEX_URL.encode('utf-8'))
        curl.setopt(PUT, 1)
        curl.perform()
        curl_http_code = curl.getinfo(HTTP_CODE)
        if curl_http_code != 200:
            raise Exception("create_elastic_index: %s\n"%(curl_http_code))
    except error:
        raise Exception("cURL operations failed during upload: %s" % curl.errstr())

def try_es_connect(attempts=0):
    """
    Recursively try to connect to elasticsearch.
    """
    try:
        curl = Curl()
        curl.setopt(URL, ES_STATUS_URL.encode('utf-8'))
        curl.perform()
        curl_http_code = curl.getinfo(HTTP_CODE)
        if curl_http_code != 200:
            raise Exception("create_elastic_index: %s\n"%(curl_http_code))
    # pylint: disable=broad-except
    except Exception, ex:
        # pylint: enable=broad-except
        if attempts < ELASTIC_CONNECT_ATTEMPTS:
            sleep(ELASTIC_WAIT)
            attempts += 1
            try_es_connect(attempts)
        else:
            raise ex
