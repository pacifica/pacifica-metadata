#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Core interface for transactioninfo metadata objects to interface with CherryPy."""
from metadata.rest.transaction_queries.transaction_lookup import TransactionLookup
from metadata.rest.transaction_queries.transaction_search import TransactionSearch
from metadata.rest.transaction_queries.transaction_last import TransactionLast
from metadata.rest.transaction_queries.file_lookup import FileLookup
from metadata.rest.transaction_queries.transactions_multi_search import TransactionsMultiSearch


# pylint: disable=too-few-public-methods
class TransactionInfoAPI(object):
    """TransactionInfoAPI API."""

    exposed = True

    def __init__(self):
        """Create local objects for subtree items."""
        self.by_id = TransactionLookup()
        self.search = TransactionSearch()
        self.files = FileLookup()
        self.last = TransactionLast()
        self.multisearch = TransactionsMultiSearch()
