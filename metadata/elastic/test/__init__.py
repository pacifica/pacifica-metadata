#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Elastic Search module."""

ES_CLUSTER_BODY = {
    'cluster_name': 'elasticsearch',
    'nodes': {
        'qQooKRbMTbqhyaTx_qWQmw': {
            'name': 'Ivan Kragoff',
            'transport_address': '127.0.0.1:9300',
            'host': '127.0.0.1',
            'ip': '127.0.0.1',
            'version': '2.4.5',
            'build': 'c849dd1',
            'http_address': '127.0.0.1:9200',
            'http': {
                'bound_address': ['0.0.0.0:9200'],
                'publish_address': '127.0.0.1:9200',
                'max_content_length_in_bytes': 104857600
            }
        }
    }
}
