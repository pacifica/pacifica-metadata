#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Update Schema from 2.0 to 3.0."""
import uuid
from peewee import ForeignKeyField, UUIDField
from playhouse.migrate import SchemaMigrator, migrate
from ..relationships import Relationships
from ..transaction_user import TransactionUser
from ..data_sources import DataSources
from ..instrument_data_source import InstrumentDataSource
from ..instrument_key_value import InstrumentKeyValue
from ..globals import DB


def _rename_columns():
    column_rename = {
        'contributors': {'person_id': 'user_id'},
        'institutionuser': {'person_id': 'user_id'},
        'instrumentuser': {'custodian_id': 'user_id'},
        'projectuser': {'person_id': 'user_id'},
        'transactionuser': {'authorized_person_id': 'user_id'}
    }
    migrator = SchemaMigrator(DB)
    for table_name, column_tre in column_rename.items():
        for old_name, new_name in column_tre.items():
            migrate(migrator.rename_column(table_name, old_name, new_name))
            old_fkey_name = '_'.join([table_name, old_name, 'fkey'])
            new_fkey_name = '_'.join([table_name, new_name, 'fkey'])
            DB.execute_sql('alter table {} rename constraint {} TO {}'.format(table_name, old_fkey_name, new_fkey_name))
            old_index_name = '_'.join([table_name, old_name])
            new_index_name = '_'.join([table_name, new_name])
            DB.execute_sql('alter index {} rename to {}'.format(old_index_name, new_index_name))


def _rename_tables():
    table_rename = {
        'institutionperson': 'institutionuser',
        'instrumentcustodian': 'instrumentuser',
        'projectparticipant': 'projectuser',
        'transactionrelease': 'transactionuser'
    }
    migrator = SchemaMigrator(DB)
    for old_table, new_table in table_rename.items():
        migrate(migrator.rename_table(old_table, new_table))
        for index_meta in DB.get_indexes(new_table):
            new_index_name = '{}{}'.format(new_table, index_meta.name[len(old_table):])
            DB.execute_sql('alter index {} rename to {}'.format(index_meta.name, new_index_name))
        for fkey_meta in DB.get_foreign_keys(new_table):
            old_name = '_'.join([old_table, fkey_meta.column, 'fkey'])
            new_name = '_'.join([new_table, fkey_meta.column, 'fkey'])
            DB.execute_sql('alter table {} rename constraint {} TO {}'.format(new_table, old_name, new_name))


def _create_tables():
    Relationships.create_table()
    DataSources.create_table()
    InstrumentDataSource.create_table()
    InstrumentKeyValue.create_table()


def _add_relationship_columns():
    table_rel = {
        'institutionuser': ('member_of', 'institution_user'),
        'instrumentuser': ('custodian', 'instrument_user'),
        'projectuser': ('member_of', 'project_user'),
        'projectinstrument': ('member_of', 'project_instrument'),
        'transactionuser': ('authorized_releaser', 'transaction_user')
    }
    migrator = SchemaMigrator(DB)
    DB.execute_sql('alter table citationtransaction drop constraint citationtransaction_transaction_id_fkey')
    DB.execute_sql('drop index citationtransaction_transaction_id')
    DB.execute_sql('alter table doitransaction drop constraint doitransaction_transaction_id_fkey')
    DB.execute_sql('drop index doitransaction_transaction_id')
    migrate(
        migrator.rename_column('citationtransaction', 'transaction_id', 'trans_old_id'),
        migrator.rename_column('doitransaction', 'transaction_id', 'trans_old_id')
    )
    for table_name, rel_info in table_rel.items():
        DB.execute_sql('alter table {} drop constraint {}_pkey'.format(table_name, table_name))
        rel_name, backref = rel_info
        rel_obj = Relationships.get(Relationships.name == rel_name)
        migrate(
            migrator.add_column(
                table_name, 'relationship_id',
                ForeignKeyField(Relationships, field=Relationships.uuid, default=rel_obj.uuid, backref=backref)
            ),
            migrator.add_column(
                table_name, 'uuid',
                UUIDField(primary_key=True, default=uuid.uuid4, index=True)
            ),
            migrator.add_index(
                table_name,
                [fkey_meta.column for fkey_meta in DB.get_foreign_keys(table_name)],
                unique=True
            )
        )
    migrate(
        migrator.add_column(
            'citationtransaction', 'transaction_id',
            ForeignKeyField(TransactionUser, default=None, null=True, field=TransactionUser.uuid)
        ),
        migrator.add_column(
            'doitransaction', 'transaction_id',
            ForeignKeyField(TransactionUser, default=None, null=True, field=TransactionUser.uuid)
        )
    )


def update_schema():
    """Update schema from 2.0 to 3.0."""
    _rename_tables()
    _rename_columns()
    _create_tables()
    _add_relationship_columns()
