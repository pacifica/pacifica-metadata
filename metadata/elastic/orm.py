#!/usr/bin/python
"""
Elastic search core class to convert db object.
"""
from StringIO import StringIO
from pycurl import Curl, URL, READFUNCTION, UPLOAD
from pycurl import INFILESIZE_LARGE, HTTP_CODE, error, PUT
from os import getenv

DEFAULT_ELASTIC_ENDPOINT = getenv('ELASTICDB_PORT', 'tcp://127.0.0.1:9200').replace('tcp', 'http')
ELASTIC_ENDPOINT = getenv('ELASTIC_ENDPOINT', DEFAULT_ELASTIC_ENDPOINT)
ELASTIC_INDEX = 'pacifica'

class ElasticAPI(object):
    """
    Elastic search conversion and interface methods.
    """
    @classmethod
    def create_elastic_index(cls):
        """
        take the elastic search mapping from the object and
        create an elastic search index with it.
        PUT /{index}/_mapping/{type}
        { body }
        """
        es_mapping_str = cls.elastic_mapping()
        es_mapping_len = len(es_mapping_str)
        elastic_mapping = StringIO(es_mapping_str)
        class_name = cls.__name__
        try:
            curl = Curl()
            es_index_url = "%s/%s/_mapping/%s"%(ELASTIC_ENDPOINT, ELASTIC_INDEX, class_name)
            curl.setopt(URL, es_index_url.encode('utf-8'))
            curl.setopt(PUT, 1)
            curl.setopt(UPLOAD, 1)
            curl.setopt(READFUNCTION, elastic_mapping.read)
            curl.setopt(INFILESIZE_LARGE, es_mapping_len)
            curl.perform()
            curl_http_code = curl.getinfo(HTTP_CODE)
            if curl_http_code != 200:
                raise Exception("create_elastic_index: %s\n"%(curl_http_code))
        except error:
            raise Exception("cURL operations failed during upload: %s" % curl.errstr())

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build elastic mapping properties hash from object.
        """
        obj['created'] = obj['updated'] = obj['deleted'] = \
        {'type': 'date', 'format': 'epoch_second'}

    @classmethod
    def elastic_mapping(cls):
        """
        Return the elasticsearch mapping for the object.
        """
        ret = {}
        obj = {}
        cls.elastic_mapping_builder(obj)
        ret['properties'] = obj
        return ret

