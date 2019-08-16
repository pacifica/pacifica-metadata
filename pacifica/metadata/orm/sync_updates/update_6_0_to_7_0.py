#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Update Schema from 6.0 to 7.0."""
from peewee import UUIDField, Model, CharField, TextField, DoesNotExist
from ..globals import DB


def _update_relationships():
    # pylint: disable=too-few-public-methods
    class OldRelationships(Model):
        """Snapshot of relationships so we can change things."""

        uuid = UUIDField(primary_key=True, index=True)
        name = CharField(default='', unique=True, index=True)
        display_name = CharField(default='', index=True)
        description = TextField(default='')
        encoding = CharField(default='UTF8')

        class Meta(object):
            """PeeWee meta class contains the database and the primary key."""

            database = DB
            table_name = 'relationships'
            legacy_table_names = False
    # pylint: enable=too-few-public-methods

    row_map = {
        'co_principle_investigator': {
            'name': 'co_principal_investigator',
            'display_name': 'Co-Principal Investigator',
            'description': 'subject is the co-principal investigator of the object'
        },
        'principle_investigator': {
            'name': 'principal_investigator',
            'display_name': 'Principal Investigator',
            'description': 'subject is the principal investigator of the object'
        },
    }
    for old_name, new_parts in row_map.items():
        try:
            rel_obj = OldRelationships.select().where(OldRelationships.name == old_name).get()
            rel_obj.name = new_parts['name']
            rel_obj.display_name = new_parts['display_name']
            rel_obj.description = new_parts['description']
            rel_obj.save()
        except DoesNotExist:
            # it may not exist since the original table was created with principal
            pass


def update_schema():
    """Update schema from 6.0 to 7.0."""
    _update_relationships()
