#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Admin tools for ElasticSearch sync."""
from __future__ import print_function
from threading import Thread
try:
    from Queue import Queue
except ImportError:
    from queue import Queue
from elasticsearch import Elasticsearch, helpers, ElasticsearchException
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


def yield_data(obj, page_number, items_per_page):
    """yield objects from obj for bulk ingest."""
    key_list = [getattr(obj, attr) for attr in obj.get_primary_keys()]
    for record in obj.select().order_by(*key_list).paginate(page_number, items_per_page):
        record_hash = record.to_hash(recursion_depth=1)
        yield {
            '_op_type': 'update',
            '_index': ELASTIC_INDEX,
            '_type': obj.__name__,
            '_id': record_hash.pop('_id'),
            'doc': record_hash,
            'doc_as_upsert': True
        }


def start_work(work_queue):
    """The main thread for the work."""
    es_client = Elasticsearch([ELASTIC_ENDPOINT], **ES_CLIENT_ARGS)
    job = work_queue.get()
    while job:
        tries_left = 5
        success = False
        while not success and tries_left:
            try:
                helpers.bulk(es_client, yield_data(*job))
                success = True
            except ElasticsearchException:
                tries_left -= 1
        if not tries_left and not success:
            print('We really failed')
        work_queue.task_done()
        print('{}: {}'.format(job[0].__name__, job[1]))
        job = work_queue.get()
    work_queue.task_done()


def essync(args):
    """Sync the elastic search data from sql to es."""
    work_queue = Queue(32)
    work_threads = []

    for i in range(args.threads):
        wthread = Thread(target=start_work, args=(work_queue,))
        wthread.daemon = True
        wthread.start()
        work_threads.append(wthread)

    for obj in args.objects:
        total_count = obj.select().count()
        num_pages = (total_count / args.items_per_page) + 1
        for page in range(1, num_pages + 1):
            work_queue.put((obj, page, args.items_per_page))

    for i in range(args.threads):
        work_queue.put(False)
    for wthread in work_threads:
        wthread.join()
    work_queue.join()
