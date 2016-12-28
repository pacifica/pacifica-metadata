#!/usr/bin/python
"""Core interface for the userinfo metadata objects to interface with CherryPy."""
from metadata.rest.user_queries.user_search import UserSearch
from metadata.rest.user_queries.user_lookup import UserLookup


# pylint: disable=too-few-public-methods
class UserInfoAPI(object):
    """UserInfo API."""

    exposed = True

    def __init__(self):
        """Create local objects for subtree items."""
        # self.by_user_id = ProposalUserSearch()
        # self.search = ProposalTermSearch()
        self.search = UserSearch()
        self.by_id = UserLookup()
