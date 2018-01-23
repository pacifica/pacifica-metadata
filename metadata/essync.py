#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Admin tools for ElasticSearch sync."""
from __future__ import print_function
from elasticsearch import Elasticsearch, helpers
from metadata.orm import ORM_OBJECTS, try_db_connect
from metadata.elastic import create_elastic_index, try_es_connect
from metadata.elastic import ELASTIC_ENDPOINT, ELASTIC_INDEX, ES_CLIENT_ARGS


def escreate(args):
    """Create the elastic search index and mappings."""
    try_db_connect()
    try_es_connect()
    create_elastic_index()
    if args.skip_mappings:
        return
    for obj in ORM_OBJECTS:
        obj.create_elastic_mapping()


def essync(args):
    """Sync the elastic search data from sql to es."""
    print(args.threads)
    es_client = Elasticsearch([ELASTIC_ENDPOINT], **ES_CLIENT_ARGS)

    def yield_data():
        """yield objects from obj for bulk ingest."""
        for obj in ORM_OBJECTS:
            for record in obj.select():
                record_hash = record.to_hash(recursion_depth=1)
                yield {
                    '_op_type': 'update',
                    '_index': ELASTIC_INDEX,
                    '_type': obj.__name__,
                    '_id': record_hash.pop('_id'),
                    'doc': record_hash,
                    'doc_as_upsert': True
                }
    helpers.bulk(es_client, yield_data())
