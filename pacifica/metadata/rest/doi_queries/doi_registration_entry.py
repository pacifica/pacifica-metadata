#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy DOI Registration Updater object class."""
from __future__ import print_function
from cherrypy import tools, request, HTTPError
from pacifica.metadata.rest.user_queries.user_search import UserSearch
from pacifica.metadata.rest.doi_queries.doi_registration_base import DOIRegistrationBase
from pacifica.metadata.orm import DOITransaction, TransactionUser, DOIInfo, Relationships
from pacifica.metadata.orm.base import DB
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
        # pylint: disable=no-member
        tr_check_query = TransactionUser().select().join(Relationships).where(
            (Relationships.name == 'authorized_releaser') &
            (TransactionUser.relationship == Relationships.uuid) &
            (TransactionUser.transaction == transaction_id)
        )
        # pylint: enable=no-member
        if tr_check_query.count() == 0:
            message = 'Transaction {0} has not been released'.format(
                transaction_id)
            raise HTTPError('400 Bad Request', message)

        # make sure this record doesn't already exist
        # add doi_entry record
        with DB.atomic():
            DOIRegistrationEntry.make_doi_entry_info(
                doi_info.get('doi'),
                meta_info,
                user_info.get('person_id')
            )

            # add doi to transaction mapping
            doi_trans_map_item = {
                'doi': doi_info.get('doi'),
                'transaction': tr_check_query.execute()[0].uuid
            }
            doi_trans_mapping, mapping_created = DOITransaction.get_or_create(
                **doi_trans_map_item)

            registration_info_item = {
                'doi': doi_info.get('doi'),
                'key': 'minting_api_id',
                'value': doi_info.get('id')
            }

            DOIInfo.get_or_create(
                **registration_info_item
            )
        return doi_trans_mapping.doi.doi, mapping_created

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
            new_entry, _created = DOIRegistrationEntry._add_doi_record_entry(
                item)
            new_entries_info.append({
                'entry': new_entry,
                'was_created': _created
            })
        return new_entries_info
