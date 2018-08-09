#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Admin tools for ElasticSearch sync."""
from __future__ import print_function
from threading import Thread
try:
    from Queue import Queue
except ImportError:  # pragma: no cover
    from queue import Queue
from math import ceil
from datetime import datetime
from elasticsearch import Elasticsearch, helpers, ElasticsearchException
from pacifica.metadata.orm import ORM_OBJECTS, try_db_connect
from pacifica.metadata.elastic import create_elastic_index, try_es_connect
from pacifica.metadata.elastic import ELASTIC_ENDPOINT, ELASTIC_INDEX, ES_CLIENT_ARGS


def escreate(args):
    """Create the elastic search index and mappings."""
    try_db_connect()
    try_es_connect()
    create_elastic_index()
    if args.skip_mappings:
        return
    for obj in ORM_OBJECTS:
        obj.create_elastic_mapping()


def yield_data(obj, page_number, items_per_page, time_ago):
    """yield objects from obj for bulk ingest."""
    key_list = [getattr(obj, attr) for attr in obj.get_primary_keys()]
    created_attr = getattr(obj, 'created')
    query = (obj
             .select()
             .where(created_attr > (datetime.now() - time_ago))
             .order_by(*key_list)
             .paginate(page_number, items_per_page))
    for record in query:
        record_hash = record.to_hash(recursion_depth=1)
        yield {
            '_op_type': 'update',
            '_index': ELASTIC_INDEX,
            '_type': obj.__name__,
            '_id': record_hash.pop('_id'),
            'doc': record_hash,
            'doc_as_upsert': True
        }


def try_doing_work(es_client, job):
    """Try doing some work even if you fail."""
    tries_left = 5
    success = False
    while not success and tries_left:
        try:
            helpers.bulk(es_client, yield_data(*job))
            success = True
        except ElasticsearchException:  # pragma: no cover
            tries_left -= 1
    return success


def start_work(work_queue):
    """The main thread for the work."""
    es_client = Elasticsearch([ELASTIC_ENDPOINT], **ES_CLIENT_ARGS)
    job = work_queue.get()
    while job:
        try_doing_work(es_client, job)
        work_queue.task_done()
        print('{}: {}'.format(job[0].__name__, job[1]))
        job = work_queue.get()
    work_queue.task_done()


def create_worker_threads(threads, work_queue):
    """Create the worker threads and return the list."""
    work_threads = []
    for i in range(threads):
        wthread = Thread(target=start_work, args=(work_queue,))
        wthread.daemon = True
        wthread.start()
        work_threads.append(wthread)
    return work_threads


def generate_work(objects, items_per_page, work_queue, time_ago):
    """Generate the work from the db and send it to the work queue."""
    for obj in objects:
        created_attr = getattr(obj, 'created')
        total_count = (obj
                       .select()
                       .where(created_attr > (datetime.now() - time_ago))
                       .count())
        num_pages = int(ceil(total_count / items_per_page))
        for page in range(1, num_pages + 1):
            work_queue.put((obj, page, items_per_page, time_ago))


def essync(args):
    """Sync the elastic search data from sql to es."""
    work_queue = Queue(32)
    work_threads = create_worker_threads(args.threads, work_queue)
    generate_work(args.objects, args.items_per_page, work_queue, args.time_ago)
    for i in range(args.threads):
        work_queue.put(False)
    for wthread in work_threads:
        wthread.join()
    work_queue.join()
