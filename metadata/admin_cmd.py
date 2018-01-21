#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Admin Module for Admin Commands."""
from __future__ import print_function
from sys import argv as sys_argv
from argparse import ArgumentParser
from metadata.orm import ORM_OBJECTS, try_db_connect
from metadata.elastic import create_elastic_index, try_es_connect


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


def main(*argv):
    """Main method for admin command line tool."""
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')
    escreate_parser = subparsers.add_parser(
        'escreate',
        help='escreate help',
        description='create elastic index and mappings'
    )
    essync_parser = subparsers.add_parser(
        'essync',
        help='essync help',
        description='sync sql data to elastic search'
    )
    essync_parser.add_argument(
        '--threads',
        default=4,
        type=int,
        help='number of threads to sync data',
        required=False
    )
    escreate_parser.add_argument(
        '--skip-mappings',
        help='skip creating mappings',
        default=False,
        action='store_true',
        dest='skip_mappings',
        required=False
    )
    escreate_parser.set_defaults(func=escreate)
    essync_parser.set_defaults(func=essync)
    if not argv:  # pragma: no cover
        argv = sys_argv[1:]
    args = parser.parse_args(argv)
    args.func(args)
