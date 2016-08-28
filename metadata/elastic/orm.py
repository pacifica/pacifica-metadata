#!/usr/bin/python
"""
Elastic search core class to convert db object.
"""
from json import dumps
import requests

from metadata.elastic import ES_INDEX_URL

class ElasticAPI(object):
    """
    Elastic search conversion and interface methods.
    """
    @classmethod
    def elastic_delete(cls, obj):
        """
        delete the object for the class in elastic search.
        """
        class_name = obj.__class__.__name__
        obj_id = obj.id
        es_obj_url = "%s/%s/%s"%(ES_INDEX_URL, class_name, str(obj_id))
        ret = requests.delete(es_obj_url.encode('utf-8'))
        if int(ret.status_code)/100 != 2:
            raise Exception("elastic_delete_obj: %s\n"%(ret.status_code))

    @classmethod
    def elastic_upload(cls, obj):
        """
        upload the object for the class to elastic search.
        """
        class_name = obj.__class__.__name__
        obj = obj.to_hash()
        obj_id = obj['_id']
        del obj['_id']
        es_obj_url = "%s/%s/%s"%(ES_INDEX_URL, class_name, str(obj_id))
        ret = requests.put(es_obj_url, data=dumps(obj))
        if int(ret.status_code)/100 != 2:
            raise Exception("upload_obj: %s\n"%(ret.status_code))

    @classmethod
    def create_elastic_mapping(cls):
        """
        take the elastic search mapping from the object and
        create an elastic search index with it.
        PUT /{index}/_mapping/{type}
        { body }
        """
        es_mapping_str = dumps(cls.elastic_mapping())
        class_name = cls.__name__
        es_mapping_url = "%s/_mapping/%s"%(ES_INDEX_URL, class_name)
        ret = requests.put(es_mapping_url.encode('utf-8'), data=es_mapping_str)
        if int(ret.status_code)/100 != 2:
            raise Exception("create_elastic_mapping: %s\n"%(ret.status_code))

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build elastic mapping properties hash from object.
        """
        obj['created'] = obj['updated'] = obj['deleted'] = \
        {'type': 'date', 'format': "yyyy-mm-dd'T'HH:mm:ss"}

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
