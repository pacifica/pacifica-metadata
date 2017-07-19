#!/usr/bin/python
"""Core interface for the proposalinfo metadata objects to interface with CherryPy."""
from metadata.rest.instrument_queries.instrument_lookup import InstrumentLookup
from metadata.rest.instrument_queries.instrument_term_search import InstrumentTermSearch
from metadata.rest.instrument_queries.instrument_user_search import InstrumentUserSearch
from metadata.rest.instrument_queries.instrument_categories import InstrumentCategories
# from metadata.rest.instrument_queries.instruments_with_category import InstrumentsWithCategory


# pylint: disable=too-few-public-methods
class InstrumentInfoAPI(object):
    """InstrumentInfo API."""

    exposed = True

    def __init__(self):
        """Create local objects for subtree items."""
        self.search = InstrumentTermSearch()
        self.by_instrument_id = InstrumentLookup()
        self.by_user_id = InstrumentUserSearch()
        self.categories = InstrumentCategories()
        # self.instruments_with_category = InstrumentsWithCategory()
