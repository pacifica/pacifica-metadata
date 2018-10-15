#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy DOI Registration Updater object class."""
from __future__ import print_function
from cherrypy import tools, request, HTTPError
from metadata.rest.user_queries.user_search import UserSearch
from metadata.rest.doi_queries.doi_registration_base import DOIRegistrationBase
from metadata.orm import DOIEntries, DOITransaction, TransactionRelease

# pylint: disable=too-few-public-methods


class DOIRegistrationEntry(DOIRegistrationBase):
    """Updates the database with new DOI registration info from registration API."""

    exposed = True

    @staticmethod
    def _add_doi_record_entry(doi_info):
        # translate existing user from network id
        user_info = UserSearch.search_for_user(
            doi_info.get('owner_network_id'), 'simple').pop()
        meta_info = doi_info.get('meta')

        infix_components = meta_info.get('doi_infix').split('.')
        transaction_id = infix_components.pop()

        # Check if transaction is released
        tr_check_query = TransactionRelease().select().where(
            TransactionRelease.transaction == transaction_id)
        if tr_check_query.count() == 0:
            message = 'Transaction {0} has not been released'.format(
                transaction_id)
            raise HTTPError('400 Bad Request', message)

        # make sure this record doesn't already exist
        # add doi_entry record
        doi_entry, _created = DOIRegistrationEntry.change_doi_entry_info(
            doi_info.get('doi'),
            meta_info,
            user_info.get('person_id')
        )

        # add doi to transaction mapping
        doi_trans_map_item = {
            'doi': doi_info.get('doi'),
            'transaction': transaction_id
        }
        doi_trans_mapping, mapping_created = DOITransaction.get_or_create(
            **doi_trans_map_item)
        return doi_trans_mapping.doi.doi, _created

    # CherryPy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    @tools.json_in()
    def POST():
        """Upload and create new DOI Entries."""
        items = request.json
        if not isinstance(items, (list,)) and isinstance(items, (dict, )):
            items = [items]
        new_entries_info = []

        for item in items:
            new_entry, _created = DOIRegistrationEntry._add_doi_record_entry(item)
            new_entries_info.append({
                'entry': new_entry,
                'was_created': _created
            })
        return new_entries_info
