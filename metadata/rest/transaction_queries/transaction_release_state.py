#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Status Transaction Metadata object class."""
from cherrypy import tools, request
from metadata.rest.transaction_queries.query_base import QueryBase
from metadata.orm import TransactionRelease
from metadata.rest.user_queries.user_lookup import UserLookup
from metadata.orm.base import db_connection_decorator


class TransactionReleaseState(QueryBase):
    """Retrieves release state for an individual transaction (GET) or set of transactions (POST)."""

    exposed = True

    @staticmethod
    def _get_release_state(transaction_list):
        output_results = {}
        # pylint: disable=no-member
        releases = (TransactionRelease
                    .select(
                        TransactionRelease.transaction,
                        TransactionRelease.authorized_person
                    )
                    .where(TransactionRelease.transaction << transaction_list).dicts())
        # pylint: enable=no-member

        user_lookup_cache = {}
        found_transactions = []
        for release in releases:
            found_transactions.append(release['transaction'])
            if release['authorized_person'] not in user_lookup_cache:
                user_lookup_cache[release['authorized_person']] = UserLookup.get_user_info_block(
                    release['authorized_person'], 'simple')
            release['person_info'] = user_lookup_cache[release['authorized_person']]
            output_results[release['transaction']] = release

        missing_transactions = list(
            set(transaction_list) - set(found_transactions))
        for txn in missing_transactions:
            output_results[txn] = {}
        return output_results

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    @db_connection_decorator
    def GET(trans_id=None):
        """Return release details about the specified transaction entity."""
        return TransactionReleaseState._get_release_state((int(trans_id),))

    @staticmethod
    @tools.json_in()
    @tools.json_out()
    @db_connection_decorator
    def POST():
        """Return transaction release state details for the list of transaction_id's."""
        transaction_list = [int(trans_id) for trans_id in request.json]
        return TransactionReleaseState._get_release_state(transaction_list)
