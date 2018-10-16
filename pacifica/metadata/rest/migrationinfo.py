#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Core interface for the proposalinfo metadata objects to interface with CherryPy."""
from pacifica.metadata.rest.migration_queries.migrate_instruments import MigrateInstruments
from pacifica.metadata.rest.migration_queries.migrate_proposals import MigrateProposals
from pacifica.metadata.rest.migration_queries.migrate_users import MigrateUsers


# pylint: disable=too-few-public-methods
class MigrationInfoAPI(object):
    """MigrationInfo API."""

    exposed = True

    def __init__(self):
        """Create local objects for subtree items."""
        self.instruments = MigrateInstruments()
        self.proposals = MigrateProposals()
        self.users = MigrateUsers()
