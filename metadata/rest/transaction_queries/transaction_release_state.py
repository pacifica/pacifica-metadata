#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Status Transaction Metadata object class."""
import re
import cherrypy
from cherrypy import tools, HTTPError, request
from metadata.rest.transaction_queries.query_base import QueryBase
from metadata.orm import TransactionRelease, DataReleaseStates
from metadata.rest.user_queries.user_lookup import UserLookup
from metadata.orm.base import db_connection_decorator


class TransactionReleaseState(QueryBase):
    """Retrieves release state for an individual transaction (GET) or set of transactions (POST)."""

    exposed = True

    @staticmethod
    def _get_release_state(transaction_list):
        if not hasattr(transaction_list, '__iter__'):
            transaction_list = [transaction_list]
        output_results = user_lookup_cache = {}
        releases = (TransactionRelease
                    .select(
                        TransactionRelease.transaction,
                        DataReleaseStates.name.alias('machine_name'),
                        DataReleaseStates.display_name,
                        TransactionRelease.person
                    )
                    .join(DataReleaseStates)
                    .where(TransactionRelease.transaction << transaction_list).dicts())

        found_transactions = []
        for release in releases:
            found_transactions.append(release['transaction'])
            if release['person'] not in user_lookup_cache:
                user_lookup_cache[release['person']] = UserLookup.get_user_info_block(
                    release['person'], 'simple')
            release['person_name'] = user_lookup_cache[release['person']]['display_name']
            output_results[release['transaction']] = release

        missing_transactions = list(
            set(transaction_list) - set(found_transactions))
        for txn in missing_transactions:
            output_results[txn] = {}
        return output_results

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    # pylint: disable=duplicate-code
    @staticmethod
    @tools.json_out()
    @db_connection_decorator
    def GET(transaction_id=None):
        """Return release details about the specified transaction entity."""
        if transaction_id and re.match('[0-9]+', transaction_id):
            return TransactionReleaseState._get_release_state(transaction_id)
        else:
            message = "Invalid transaction release lookup request. '{0}' is not a valid transaction_id".format(
                transaction_id)
            cherrypy.log.error(message)
            raise HTTPError(
                '400 Invalid Transaction ID',
                QueryBase.compose_help_block_message()
            )

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_in()
    @tools.json_out()
    @db_connection_decorator
    def POST():
        """Return transaction release state details for the list of transaction_id's."""
        transaction_list = request.json
        return TransactionReleaseState._get_release_state(transaction_list)
