#!/usr/bin/python
"""
Elastic search core class to convert db object.
"""
from StringIO import StringIO
from json import dumps
from pycurl import Curl, URL, READFUNCTION, UPLOAD, CUSTOMREQUEST
from pycurl import INFILESIZE_LARGE, HTTP_CODE, error, PUT

from metadata.elastic import ES_INDEX_URL

class ElasticAPI(object):
    """
    Elastic search conversion and interface methods.
    """
    @classmethod
    def elastic_delete(cls, obj_id):
        """
        delete the object for the class in elastic search.
        """
        class_name = cls.__name__
        es_obj_url = "%s/%s/%s"%(ES_INDEX_URL, class_name, str(obj_id))
        try:
            curl = Curl()
            curl.setopt(URL, es_obj_url.encode('utf-8'))
            curl.setopt(CUSTOMREQUEST, 'DELETE')
            curl.perform()
            curl_http_code = curl.getinfo(HTTP_CODE)
            if int(curl_http_code)/100 != 2:
                raise Exception("upload_obj: %s\n"%(curl_http_code))
        except error:
            raise Exception("cURL operations failed during upload: %s" % curl.errstr())

    @classmethod
    def elastic_upload(cls, obj):
        """
        upload the object for the class to elastic search.
        """
        obj_id = obj['_id']
        del obj['_id']
        obj_str = dumps(obj)
        obj_len = len(obj_str)
        obj_io = StringIO(obj_str)
        class_name = cls.__name__
        es_obj_url = "%s/%s/%s"%(ES_INDEX_URL, class_name, str(obj_id))
        try:
            curl = Curl()
            curl.setopt(URL, es_obj_url.encode('utf-8'))
            curl.setopt(PUT, 1)
            curl.setopt(UPLOAD, 1)
            curl.setopt(READFUNCTION, obj_io.read)
            curl.setopt(INFILESIZE_LARGE, obj_len)
            curl.perform()
            curl_http_code = curl.getinfo(HTTP_CODE)
            if int(curl_http_code)/100 != 2:
                raise Exception("upload_obj: %s\n"%(curl_http_code))
        except error:
            raise Exception("cURL operations failed during upload: %s" % curl.errstr())

    @classmethod
    def create_elastic_mapping(cls):
        """
        take the elastic search mapping from the object and
        create an elastic search index with it.
        PUT /{index}/_mapping/{type}
        { body }
        """
        es_mapping_str = dumps(cls.elastic_mapping())
        es_mapping_len = len(es_mapping_str)
        elastic_mapping = StringIO(es_mapping_str)
        class_name = cls.__name__
        es_mapping_url = "%s/_mapping/%s"%(ES_INDEX_URL, class_name)
        try:
            curl = Curl()
            curl.setopt(URL, es_mapping_url.encode('utf-8'))
            curl.setopt(PUT, 1)
            curl.setopt(UPLOAD, 1)
            curl.setopt(READFUNCTION, elastic_mapping.read)
            curl.setopt(INFILESIZE_LARGE, es_mapping_len)
            curl.perform()
            curl_http_code = curl.getinfo(HTTP_CODE)
            if int(curl_http_code)/100 != 2:
                raise Exception("create_elastic_mapping: %s\n"%(curl_http_code))
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
