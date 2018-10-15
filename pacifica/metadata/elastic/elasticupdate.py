#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Core interface for the uploader metadata objects to interface with CherryPy."""
from cherrypy import tools, request
from elasticsearch import Elasticsearch, helpers
from pacifica.metadata.elastic import ELASTIC_ENDPOINT, ELASTIC_INDEX, ES_CLIENT_ARGS
from pacifica.metadata.orm.base import db_connection_decorator
from pacifica.metadata.rest.objectinfo import ObjectInfoAPI


# pylint: disable=too-few-public-methods
class ElasticSearchUpdateAPI(object):
    """ElasticSearchUpdateAPI."""

    exposed = True

    @staticmethod
    @db_connection_decorator
    def push_elastic_updates(object_class_name, id_list, recursion_depth):
        """Push out updates to the ES cluster for updated MD records."""
        myclass = ObjectInfoAPI.get_class_object_from_name(
            object_class_name=object_class_name)
        records = myclass.select()
        if id_list:
            records.where(myclass.id << id_list)
        es_client = Elasticsearch([ELASTIC_ENDPOINT], **ES_CLIENT_ARGS)
        return helpers.bulk(es_client, ElasticSearchUpdateAPI.read_md_records(records, myclass, recursion_depth))

    @staticmethod
    def read_md_records(md_records, myclass, recursion_depth):
        """Make a generator object to be used in push_elastic_updates."""
        for record in md_records:
            record_hash = record.to_hash(recursion_depth=recursion_depth)
            yield {
                '_op_type': 'update',
                '_index': ELASTIC_INDEX,
                '_type': myclass.__name__,
                '_id': record_hash.pop('_id'),
                'doc': record_hash
            }

    # CherryPy requires these named methods.
    # pylint: disable=invalid-name, protected-access
    @staticmethod
    @tools.json_in()
    @tools.json_out()
    def POST(object_class_name, recursion_depth=1):
        """
        Implement the POST HTTP method.

        Pushes updated content to the ElasticSearch cluster.
        """
        id_list = request.json if request.json else []

        return ElasticSearchUpdateAPI.push_elastic_updates(object_class_name, id_list, recursion_depth)
