#!/usr/bin/python
"""Core interface for the proposalinfo metadata objects to interface with CherryPy."""
from metadata.rest.instrument_queries.instrument_lookup import InstrumentLookup
from metadata.rest.instrument_queries.instrument_term_search import InstrumentTermSearch


# pylint: disable=too-few-public-methods
class InstrumentInfoAPI(object):
    """InstrumentInfo API."""

    exposed = True

    def __init__(self):
        """Create local objects for subtree items."""
        self.search = InstrumentTermSearch()
        self.by_instrument_id = InstrumentLookup()
