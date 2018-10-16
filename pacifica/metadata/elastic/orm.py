#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Elastic search core class to convert db object."""
from elasticsearch import Elasticsearch, helpers
from pacifica.metadata.elastic import ELASTIC_ENDPOINT, ELASTIC_INDEX, ES_CLIENT_ARGS


class ElasticAPI(object):
    """Elastic search conversion and interface methods."""

    @classmethod
    def elastic_delete(cls, obj):
        """Delete the object for the class in elastic search."""
        class_name = obj.__class__.__name__
        obj_id = obj.id
        esclient = Elasticsearch([ELASTIC_ENDPOINT], **ES_CLIENT_ARGS)
        esclient.delete(ELASTIC_INDEX, class_name, obj_id)

    @classmethod
    def elastic_upload(cls, objs):
        """Upload the object for the class to elastic search."""
        esclient = Elasticsearch([ELASTIC_ENDPOINT], **ES_CLIENT_ARGS)
        class_name = cls.__name__
        clean_oper = []
        for obj in objs:
            oper = None
            if esclient.exists(ELASTIC_INDEX, class_name, obj['_id']):
                oper = {}
                oper['_op_type'] = 'update'
                oper['doc'] = obj
            else:
                oper = obj
                oper['_op_type'] = 'create'
            oper['_index'] = ELASTIC_INDEX
            oper['_type'] = class_name
            oper['_id'] = obj.pop('_id')
            clean_oper.append(oper)
        helpers.bulk(esclient, clean_oper, True)

    @classmethod
    def create_elastic_mapping(cls):
        """
        Create elastic search index from object mappings.

        Take the elastic search mapping from the object and
        create an elastic search index with it.
        PUT /{index}/_mapping/{type}
        { body }
        """
        class_name = cls.__name__
        esclient = Elasticsearch([ELASTIC_ENDPOINT], **ES_CLIENT_ARGS)
        esclient.indices.put_mapping(
            class_name, cls.elastic_mapping(), ELASTIC_INDEX)

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build elastic mapping properties hash from object."""
        obj['created'] = obj['updated'] = obj['deleted'] = \
            {'type': 'date', 'format': "yyyy-mm-dd'T'HH:mm:ss"}

    @classmethod
    def elastic_mapping(cls):
        """Return the elasticsearch mapping for the object."""
        ret = {}
        obj = {}
        cls.elastic_mapping_builder(obj)
        ret['properties'] = obj
        return ret
