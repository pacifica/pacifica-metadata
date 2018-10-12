#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Core interface to upload DOI registration info into metadata with CherryPy."""
from metadata.rest.doi_queries.doi_registration_update import DOIRegistrationUpdate


# pylint: disable=too-few-public-methods
class DOIUploadAPI(object):
    """InstrumentInfo API."""

    exposed = True

    def __init__(self):
        """Create local objects for subtree items."""
        self.upload_info = DOIRegistrationUpdate
