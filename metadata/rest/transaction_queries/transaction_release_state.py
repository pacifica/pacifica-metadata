#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Status Transaction Metadata object class."""
from cherrypy import tools, request
from metadata.rest.transaction_queries.query_base import QueryBase
from metadata.orm import TransactionRelease, DOIRelease, CitationRelease
from metadata.rest.user_queries.user_lookup import UserLookup
from metadata.orm.base import db_connection_decorator


class TransactionReleaseState(QueryBase):
    """Retrieves release state for an individual transaction (GET) or set of transactions (POST)."""

    exposed = True
    user_lookup_cache = {}

    @staticmethod
    def _get_release_state(transaction_list):
        releases = TransactionReleaseState._get_release_info(transaction_list)

        output_results = {}
        found_transactions = []

        for release in releases:
            found_transactions.append(release['transaction'])
            if release['authorized_person'] not in self.user_lookup_cache:
                self.user_lookup_cache[release['authorized_person']] = UserLookup.get_user_info_block(
                    release['authorized_person'], 'simple')
            release.update({
                'authorized_person': self.user_lookup_cache[release['authorized_person']],
                'release_state': 'released', 'display_state': 'Released',
                'release_doi_entries': TransactionReleaseState._get_doi_release(release['release_id']),
                'release_citations': TransactionReleaseState._get_citation_release(release['release_id'])
            })
            output_results[release['transaction']] = release

        missing_transactions = list(set(transaction_list) - set(found_transactions))
        for txn in missing_transactions:
            output_results[txn] = {
                'authorized_person': None, 'release_id': None, 'release_state': 'not_released',
                'display_state': 'Not Released', 'transaction': txn
            }

        return output_results

    @staticmethod
    def _get_release_info(transaction_list):
        # pylint: disable=no-member
        releases = (TransactionRelease
                    .select(TransactionRelease.id.alias('release_id'), TransactionRelease.transaction,
                            TransactionRelease.authorized_person
                            )
                    .where(TransactionRelease.transaction << transaction_list).dicts())
        # pylint: enable=no-member
        return releases

    @staticmethod
    def _get_doi_release(release_id):
        output_results = []
        # pylint: disable=no-member
        doi_releases = (DOIRelease
                        .select()
                        .where(DOIRelease.release_id == release_id))
        # pylint: enable=no-member
        if doi_releases.exists():
            for release in doi_releases:
                output_results.append({
                    'doi_name': release.doi.name,
                    'doi_reference': release.doi.doi
                })
        else:
            output_results = None
        return output_results

    @staticmethod
    def _get_citation_release(release_id):
        output_results = []
        # pylint: disable=no-member
        citation_releases = (CitationRelease
                             .select()
                             .where(CitationRelease.release_id == release_id))
        # pylint: enable=no-member
        if citation_releases.exists():
            for citation_entry in citation_releases:
                output_results.append(
                    {
                        'citation_id': citation_entry.citation.id,
                        'title': citation_entry.citation.article_title,
                        'doi_reference': citation_entry.citation.doi_reference
                    }
                )
        else:
            output_results = None
        return output_results

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    @db_connection_decorator
    def GET(trans_id=None):
        """Return release details about the specified transaction entity."""
        return TransactionReleaseState._get_release_state((int(trans_id),))

    # pylint: disable=duplicate-code
    @staticmethod
    @tools.json_out()
    @tools.json_in()
    @db_connection_decorator
    # pylint: enable=duplicate-code
    def POST():
        """Return transaction release state details for the list of transaction_id's."""
        transaction_list = [int(trans_id) for trans_id in request.json]
        return TransactionReleaseState._get_release_state(transaction_list)
