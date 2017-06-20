#!/usr/bin/python
"""Core interface for the tkvinfo metadata objects to interface with CherryPy."""
from metadata.rest.tkvinfo_queries.values_for_key import ValuesForKey
from metadata.rest.tkvinfo_queries.upload_entries import UploadEntries


# pylint: disable=too-few-public-methods
class TkvInfoAPI(object):
    """InstrumentInfo API."""

    exposed = True

    def __init__(self):
        """Create local objects for subtree items."""
        self.values_for_key = ValuesForKey()
        self.upload_entries = UploadEntries
