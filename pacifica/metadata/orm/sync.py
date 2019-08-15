#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The ORM Sync Module."""
from time import sleep
from types import MethodType
from importlib import import_module
from peewee import OperationalError, CharField, IntegerField, Model
from ..config import get_config
from .globals import DB
from .all_objects import ORM_OBJECTS

SCHEMA_MAJOR = 7
SCHEMA_MINOR = 0

# pylint: disable=too-few-public-methods


class OrmSync(object):
    """
    Special module for syncing the orm.

    This module should incorporate a schema migration strategy.

    The supported versions migrating forward must be in a versions array
    containing tuples for major and minor versions.

    The version tuples are directly translated to method names in the
    orm_update class for the update between those versions.

    Example Methods::

      class OrmSync:
        versions = [
          (0, 1),
          (0, 2),
          (1, 0),
          (1, 1)
        ]

        def update_0_1_to_0_2():
          pass
        def update_0_2_to_1_0():
          pass

    The body of the update should follow peewee migration practices.
    http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#migrate
    """

    method_format = 'update_{}_to_{}'
    versions = [
        (0, 1),
        (1, 0),
        (2, 0),
        (2, 1),
        (3, 0),
        (4, 0),
        (5, 0),
        (6, 0),
        (7, 0)
    ]

    @staticmethod
    def dbconn_blocking():
        """Wait for the db connection."""
        dbcon_attempts = get_config().getint('database', 'connect_attempts')
        dbcon_wait = get_config().getint('database', 'connect_wait')
        while dbcon_attempts:
            try:  # pragma: no cover this block doesn't complete
                if not DB.is_closed():
                    DB.close()
                DB.connect()
                return
            except OperationalError:
                # couldnt connect, potentially wait and try again
                sleep(dbcon_wait)
                dbcon_attempts -= 1
        raise OperationalError('Failed database connect retry.')

    @classmethod
    def update_tables(cls):
        """Update the database to the current version."""
        verlist = cls.versions
        db_ver = MetadataSystem.get_version()
        if verlist.index(verlist[-1]) == verlist.index(db_ver):
            # we have the current version don't update
            return
        with DB.atomic():
            for db_ver in verlist[verlist.index(db_ver):-1]:
                next_db_ver = verlist[verlist.index(db_ver)+1]
                getattr(cls, cls.method_format.format(
                    '{}_{}'.format(*db_ver),
                    '{}_{}'.format(*next_db_ver)
                ))()
            MetadataSystem.drop_table()
            MetadataSystem.create_table()
            MetadataSystem.get_or_create_version()

    @staticmethod
    def create_tables():
        """Create the tables for the objects if they exist."""
        with DB.atomic():
            MetadataSystem.create_table()
            MetadataSystem.get_or_create_version()
            for obj in ORM_OBJECTS:
                if not obj.table_exists():
                    obj.create_table()

    @staticmethod
    def close():
        """Close the database connection."""
        DB.close()

    @classmethod
    def connect_and_check(cls):
        """Connect and check the version."""
        cls.dbconn_blocking()
        if not MetadataSystem.is_safe():  # pragma: no cover the raise prevents coverage
            cls.close()
            raise OperationalError('Database version too old {} update to {}'.format(
                '{}.{}'.format(*(MetadataSystem.get_version())),
                '{}.{}'.format(SCHEMA_MAJOR, SCHEMA_MINOR)
            ))


for ver_index in range(len(OrmSync.versions)-1):
    def update_version(cls, index=ver_index):
        """Update to the schema to create relationships."""
        old_ver = cls.versions[index]
        new_ver = cls.versions[index+1]
        mod_name = '.sync_updates.update_{}_to_{}'.format('{}_{}'.format(*old_ver), '{}_{}'.format(*new_ver))
        module = import_module(mod_name, 'pacifica.metadata.orm')
        module.update_schema()
    old_version = OrmSync.versions[ver_index]
    new_version = OrmSync.versions[ver_index+1]
    setattr(
        OrmSync,
        OrmSync.method_format.format(
            '{}_{}'.format(*old_version),
            '{}_{}'.format(*new_version)
        ), MethodType(update_version, OrmSync)
    )


class MetadataSystem(Model):
    """Metadata Schema Version Model."""

    part = CharField(primary_key=True)
    value = IntegerField(default=-1)

    class Meta(object):
        """Meta object containing the database connection."""

        database = DB  # This model uses the pacifica_cart database.

    @classmethod
    def get_or_create_version(cls):
        """Set or create the current version of the schema."""
        major = cls.get_or_create(part='major', value=SCHEMA_MAJOR)
        minor = cls.get_or_create(part='minor', value=SCHEMA_MINOR)
        return (major, minor)

    @classmethod
    def get_version(cls):
        """Get the current version as a tuple."""
        return (cls.get(part='major').value, cls.get(part='minor').value)

    @classmethod
    def is_equal(cls):
        """Check to see if schema version matches code version."""
        major, minor = cls.get_version()
        return major == SCHEMA_MAJOR and minor == SCHEMA_MINOR

    @classmethod
    def is_safe(cls):
        """Check to see if the schema version is safe for the code."""
        major, _minor = cls.get_version()
        return major == SCHEMA_MAJOR
