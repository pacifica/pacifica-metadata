#!/usr/bin/python
"""
Elastic search core class to convert db object.
"""
from elasticsearch import Elasticsearch

from metadata.elastic import ELASTIC_ENDPOINT, ELASTIC_INDEX

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
        esclient = Elasticsearch([ELASTIC_ENDPOINT])
        esclient.delete(ELASTIC_INDEX, class_name, obj_id)

    @classmethod
    def elastic_upload(cls, obj):
        """
        upload the object for the class to elastic search.
        """
        class_name = obj.__class__.__name__
        obj = obj.to_hash()
        obj_id = obj['_id']
        del obj['_id']
        esclient = Elasticsearch([ELASTIC_ENDPOINT])
        if esclient.exists(ELASTIC_INDEX, class_name, obj_id):
            esclient.update(ELASTIC_INDEX, class_name, obj_id, obj)
        else:
            esclient.create(ELASTIC_INDEX, class_name, obj_id, obj)

    @classmethod
    def create_elastic_mapping(cls):
        """
        take the elastic search mapping from the object and
        create an elastic search index with it.
        PUT /{index}/_mapping/{type}
        { body }
        """
        class_name = cls.__name__
        esclient = Elasticsearch([ELASTIC_ENDPOINT])
        esclient.indices.put_mapping(class_name, cls.elastic_mapping())

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
