#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Configuration reading and validation module."""
from os import getenv
try:
    from ConfigParser import SafeConfigParser
except ImportError:  # pragma: no cover python 2 vs 3 issue
    from configparser import SafeConfigParser
from pacifica.metadata.globals import CONFIG_FILE


def get_config():
    """
    Return the ConfigParser object with defaults set.

    Currently metadata API doesn't work with SQLite the queries are
    too complex and it only is supported with MySQL and PostgreSQL.
    """
    configparser = SafeConfigParser()
    configparser.add_section('database')
    configparser.set('database', 'peewee_url', getenv(
        'PEEWEE_URL', 'postgresql://pacifica:metadata@localhost:5432/pacifica_metadata'))
    configparser.add_section('notifications')
    configparser.set('notifications', 'url', getenv(
        'NOTIFICATIONS_URL', 'http://127.0.0.1:8070/receive'))
    configparser.add_section('elasticsearch')
    configparser.set('elasticsearch', 'url', getenv(
        'ELASTIC_ENDPOINT', 'http://127.0.0.1:9200'))
    configparser.read(CONFIG_FILE)
    return configparser
