#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Admin Module for Admin Commands."""
from __future__ import print_function
from sys import argv as sys_argv
from json import loads, dumps
from argparse import ArgumentParser
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


def render_obj(args):
    """Render an object based on args."""
    print(dumps(args.object.get(args.object.where_clause(args.where_clause)), indent=4))


def create_subcommands(subparsers):
    """Create the subcommands from the subparsers."""
    render_parser = subparsers.add_parser(
        'render',
        help='render help',
        description='render and object from database w/o API'
    )
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
    return render_parser, escreate_parser, essync_parser


def escreate_options(escreate_parser):
    """Add the escreate command line options."""
    escreate_parser.add_argument(
        '--skip-mappings',
        help='skip creating mappings',
        default=False,
        action='store_true',
        dest='skip_mappings',
        required=False
    )
    escreate_parser.set_defaults(func=escreate)


def essync_options(essync_parser):
    """Add the essync command line options."""
    essync_parser.add_argument(
        '--threads',
        default=4,
        type=int,
        help='number of threads to sync data',
        required=False
    )
    essync_parser.set_defaults(func=essync)


def objstr_to_ormobj(obj_str):
    """Convert a string to an orm object or raise ValueError."""
    obj_strs = [obj.__name__ for obj in ORM_OBJECTS]
    if str(obj_str) not in obj_strs:
        raise ValueError('{} not a valid Metadata Object.'.format(obj_str))
    return [obj for obj in ORM_OBJECTS if obj.__name__ == str(obj_str)][0]


def objstr_to_whereclause(obj_str):
    """Convert a string to a where clause hash or raise ValueError."""
    json_obj = loads(obj_str)
    if not isinstance(json_obj, dict):
        raise ValueError('{} should be a dict not {}'.format(
            json_obj, type(json_obj)))
    return json_obj


def render_options(render_parser):
    """Add the essync command line options."""
    render_parser.add_argument(
        '--object-name',
        dest='object',
        type=objstr_to_ormobj,
        help='object type to query.',
        required=True
    )
    render_parser.add_argument(
        '--where-clause',
        dest='where_clause',
        type=objstr_to_whereclause,
        help='query to use.',
        required=True
    )
    render_parser.add_argument(
        '--recursive',
        default=1,
        type=int,
        help='recursive level to go',
        required=False
    )
    render_parser.set_defaults(func=render_obj)


def main(*argv):
    """Main method for admin command line tool."""
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')
    render_parser, escreate_parser, essync_parser = create_subcommands(
        subparsers)
    escreate_options(escreate_parser)
    essync_options(essync_parser)
    render_options(render_parser)
    if not argv:  # pragma: no cover
        argv = sys_argv[1:]
    args = parser.parse_args(argv)
    args.func(args)
