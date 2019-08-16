#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Update Schema from 4.0 to 5.0."""
from playhouse.migrate import SchemaMigrator, migrate
from ..datasets import Datasets
from ..dataset_file import DatasetFile
from ..dataset_project_user import DatasetProjectUser
from ..globals import DB


def _rename_column():
    table_name = 'usergroup'
    old_name = 'person_id'
    new_name = 'user_id'
    migrator = SchemaMigrator(DB)
    migrate(migrator.rename_column(table_name, old_name, new_name))
    old_fkey_name = '_'.join([table_name, old_name, 'fkey'])
    new_fkey_name = '_'.join([table_name, new_name, 'fkey'])
    DB.execute_sql('alter table {} rename constraint {} TO {}'.format(table_name, old_fkey_name, new_fkey_name))
    old_index_name = '_'.join([table_name, old_name])
    new_index_name = '_'.join([table_name, new_name])
    DB.execute_sql('alter index {} rename to {}'.format(old_index_name, new_index_name))


def _create_tables():
    Datasets.create_table()
    DatasetFile.create_table()
    DatasetProjectUser.create_table()


def update_schema():
    """Update schema from 4.0 to 5.0."""
    _rename_column()
    _create_tables()
