#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Admin Module for Admin Commands."""
from __future__ import print_function
from sys import argv as sys_argv
from datetime import timedelta
from json import loads, dumps
from argparse import ArgumentParser
from peewee import PeeweeException
from .orm.all_objects import ORM_OBJECTS
from .orm.sync import OrmSync, MetadataSystem
from .elastic import try_es_connect, create_elastic_index
from .essync import escreate, essync


def render_obj(args):
    """Render an object based on args."""
    OrmSync.connect_and_check()
    test_obj = args.object()
    test_obj = args.object.get(
        test_obj.where_clause(args.where_clause)
    )
    print(
        dumps(
            test_obj.to_hash(recursion_depth=args.recursion),
            indent=4
        )
    )
    if args.delete:
        test_obj.delete_instance()
        test_obj.elastic_delete(test_obj)


def create_obj(args):
    """Create a specific object."""
    OrmSync.dbconn_blocking()
    try_es_connect()
    create_elastic_index()
    if not args.object.table_exists():
        args.object.create_table()


def bool2cmdint(command_bool):
    """Convert a boolean to either 0 for true  or -1 for false."""
    if command_bool:
        return 0
    return -1


def dbchk(args):
    """Check the database for the version running."""
    OrmSync.dbconn_blocking()
    if args.check_equal:
        res = MetadataSystem.is_equal()
        OrmSync.close()
        return bool2cmdint(res)
    res = MetadataSystem.is_safe()
    OrmSync.close()
    return bool2cmdint(res)


def dbsync(_args):
    """Create or update the database."""
    OrmSync.dbconn_blocking()
    try:
        MetadataSystem.get_version()
    except PeeweeException:
        OrmSync.dbconn_blocking()
        try_es_connect()
        create_elastic_index()
        OrmSync.create_tables()
        OrmSync.close()
        return
    OrmSync.update_tables()
    OrmSync.close()
    return


def create_subcommands(subparsers):
    """Create the subcommands from the subparsers."""
    create_obj_parser = subparsers.add_parser(
        'create_obj',
        help='create_obj help',
        description='create an object in the DB'
    )
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
    db_parser = subparsers.add_parser(
        'dbsync',
        help='dbsync help',
        description='Update or Create the Database.'
    )
    dbchk_parser = subparsers.add_parser(
        'dbchk',
        help='dbchk help',
        description='Check database against current version.'
    )
    return (
        (render_parser, render_options),
        (escreate_parser, escreate_options),
        (essync_parser, essync_options),
        (create_obj_parser, create_obj_options),
        (db_parser, db_options),
        (dbchk_parser, dbchk_options)
    )


def db_options(db_parser):
    """Add the options for dbsync subcommand."""
    db_parser.set_defaults(func=dbsync)


def dbchk_options(dbchk_parser):
    """Add the options for dbchk."""
    dbchk_parser.add_argument(
        '--equal', default=False,
        dest='check_equal', action='store_true'
    )
    dbchk_parser.set_defaults(func=dbchk)


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
        '--objects-per-page', default=40000,
        type=int, help='objects per bulk upload.',
        required=False, dest='items_per_page'
    )
    essync_parser.add_argument(
        '--threads', default=4, required=False,
        type=int, help='number of threads to sync data',
    )
    essync_parser.add_argument(
        '--object-name', dest='objects', type=objstr_to_ormobj,
        help='object type to sync.', required=False, nargs='*',
        default=ORM_OBJECTS
    )
    essync_parser.add_argument(
        '--time-ago', dest='time_ago', type=objstr_to_timedelta,
        help='only objects newer than X days ago.', required=False,
        default=timedelta(days=36500)
    )
    essync_parser.set_defaults(func=essync)


def objstr_to_timedelta(obj_str):
    """Turn an object string of the format X unit ago into timedelta."""
    value, unit, check = obj_str.split()
    assert check == 'ago'
    return timedelta(**{unit: float(value)})


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


def create_obj_options(create_obj_parser):
    """Add the create object command line options."""
    create_obj_parser.add_argument(
        '--object-name',
        dest='object',
        type=objstr_to_ormobj,
        help='object type to query.',
        required=True
    )
    create_obj_parser.set_defaults(func=create_obj)


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
        '--recursion',
        default=1,
        dest='recursion',
        type=int,
        help='recursive level to go',
        required=False
    )
    render_parser.add_argument(
        '--delete',
        default='store_false',
        action='store_true',
        dest='delete',
        help='delete the object',
        required=False
    )
    render_parser.set_defaults(func=render_obj)


def main(*argv):
    """Main method for admin command line tool."""
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')
    for subparser, options_func in create_subcommands(subparsers):
        options_func(subparser)
    if not argv:  # pragma: no cover
        argv = sys_argv[1:]
    args = parser.parse_args(argv)
    return args.func(args)
