#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Update Schema from 5.0 to 6.0."""
from ..globals import DB


def _update_relationships():
    row_map = {
        'co_principle_investigator': 'co_principal_investigator',
        'principle_investigator': 'principal_investigator'
    }
    for old_val, new_val in row_map.items():
        DB.execute_sql('update relationships set name = \'?\' where name = \'?\';', (new_val, old_val))


def _lower_email_address():
    DB.execute_sql('update users set email_address = lower(email_address);')


def update_schema():
    """Update schema from 4.0 to 5.0."""
    _update_relationships()
    _lower_email_address()
