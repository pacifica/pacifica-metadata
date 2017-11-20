#!/usr/bin/python
"""Core interface for the uploader metadata objects to interface with CherryPy."""
from cherrypy import tools, request
from elasticsearch import Elasticsearch, helpers
from metadata.elastic import ELASTIC_ENDPOINT, ELASTIC_INDEX, ES_CLIENT_ARGS
from metadata.orm.base import db_connection_decorator
from metadata.rest.objectinfo import ObjectInfoAPI


# pylint: disable=too-few-public-methods
class ElasticSearchUpdateAPI(object):
    """ElasticSearchUpdateAPI."""

    exposed = True

    @staticmethod
    @db_connection_decorator
    def push_elastic_updates(object_class_name, id_list, recursion_depth):
        """Push out updates to the ES cluster for updated MD records."""
        myclass = ObjectInfoAPI.get_class_object_from_name(object_class_name=object_class_name)
        records = myclass.select()
        if id_list:
            records.where(myclass.id << id_list)
        es_client = Elasticsearch([ELASTIC_ENDPOINT], **ES_CLIENT_ARGS)
        update_list = ({
            '_op_type': 'update',
            '_index': ELASTIC_INDEX,
            '_type': myclass.__name__,
            '_id': r.pop('_id'),
            'doc': r
        } for r in ElasticSearchUpdateAPI.read_md_records(records, recursion_depth))

        return helpers.bulk(es_client, update_list)

    @staticmethod
    def read_md_records(md_records, recursion_depth):
        """Make a generator object to be used in push_elastic_updates."""
        for record in md_records:
            record_dict = record.to_hash(recursion_depth)
            yield record_dict

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
