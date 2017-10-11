#!/usr/bin/python
"""Core interface for the uploader metadata objects to interface with CherryPy."""
from os import getenv
from cherrypy import tools, request
from elasticsearch import Elasticsearch, helpers
from metadata.orm.base import db_connection_decorator
from metadata.rest.objectinfo import ObjectInfoAPI

ELASTIC_CONNECT_ATTEMPTS = 40
ELASTIC_WAIT = 3
DEFAULT_ELASTIC_ENDPOINT = getenv('ELASTICDB_PORT', 'tcp://127.0.0.1:9200').replace('tcp', 'http')
ELASTIC_ENDPOINT = getenv('ELASTIC_ENDPOINT', DEFAULT_ELASTIC_ENDPOINT)
ELASTIC_INDEX = getenv('ELASTIC_INDEX', 'pacifica')
ES_INDEX_URL = '{0}/{1}'.format(ELASTIC_ENDPOINT, ELASTIC_INDEX)


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
        es_client = Elasticsearch([ELASTIC_ENDPOINT])
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
