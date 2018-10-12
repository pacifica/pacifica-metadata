#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy DOI Registration Updater object class."""
from __future__ import print_function
from peewee import fn
from cherrypy import tools, request, HTTPError
import requests
from dateutil.parser import parse
from metadata.rest.user_queries.user_search import UserSearch
from metadata.orm import DOIEntries, DOITransaction, TransactionRelease
from metadata.orm import DOIAuthors, DOIAuthorMapping, DOIInfo
from xml.etree import ElementTree
import pprint


class DOIRegistrationUpdate(object):
    """Updates the database with new DOI registration info from registration API."""

    exposed = True

    @staticmethod
    def _add_doi_record_entry(doi_info):
        # translate existing user from network id
        user_info = UserSearch.search_for_user(doi_info.get('owner_network_id'), 'simple').pop()
        user_id = user_info.get('person_id')
        meta_info = doi_info.get('meta')

        infix_components = meta_info.get('doi_infix').split('.')
        transaction_id = infix_components.pop()

        # Check if transaction is released
        tr_check_query = TransactionRelease().select().where(TransactionRelease.transaction == transaction_id)
        if tr_check_query.count() == 0:
            message = 'Transaction {0} has not been released'.format(transaction_id)
            raise HTTPError('400 Bad Request', message)

        # make sure this record doesn't already exist
        # add doi_entry record
        DOIRegistrationUpdate._update_doi_entry_info(
            doi_info.get('doi'),
            meta_info,
            user_info.get('person_id')
        )

        # add doi to transaction mapping
        doi_trans_map_item = {
            'doi': doi_info.get('doi'),
            'transaction': transaction_id
        }
        doi_trans_mapping, mapping_created = DOITransaction.get_or_create(**doi_trans_map_item)
        return doi_trans_mapping.doi.doi

    @staticmethod
    def _get_updated_osti_info(doi_string, elink_url, elink_user, elink_password):
        """This will access the server at OSTI and get all the relevant details for this DOI."""
        osti_elink_url = elink_url + '?doi=' + doi_string

        r = requests.get(osti_elink_url, auth=(elink_user, elink_password))
        tree = ElementTree.fromstring(r.content)

        record = tree[0]
        current_status = record.attrib['status'].lower()
        release_status = record.attrib['released'].lower() == 'y'

        doi_info = {}
        for child in record:
            if child.tag == 'creatorsblock':
                # these are authors, handle appropriately
                DOIRegistrationUpdate._extract_authors(child)
                continue
            elif 'date' in child.tag:
                info = parse(child.text).strftime('%Y-%m-%d')
            else:
                info = child.text
            doi_info[child.tag] = info

        DOIRegistrationUpdate._update_doi_metadata_info(doi_info, doi_string)
        DOIRegistrationUpdate._update_doi_entry_info(
            doi_string, doi_info, None, current_status, release_status)

    @staticmethod
    def _extract_authors(creatorsblock_element, doi_string):
        author_list = [{x.tag: x.text for x in el} for el in creatorsblock_element]
        DOIRegistrationUpdate._update_author_info(author_list, doi_string)

    @staticmethod
    def _update_author_info(author_list, doi_string):
        # cross check author list with doi_authors
        # adding new and retrieving existing
        author_info_mapping = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'affiliation_name': 'affiliation',
            'private_email': 'email',
            'orcid_id': 'orcid'
        }
        author_id_list = []
        for author_info in author_list:
            my_author_info = {}
            for key in author_info:
                my_key = author_info_mapping[key]
                my_author_info[my_key] = author_info[key]
            author, _created = DOIAuthors.get_or_create(**my_author_info)
            author_id_list.append(author.id)

        # add doi to author mappings
        author_order = 0
        for author_id in author_id_list:
            author_order += 1
            author_map_insert_item = {
                'author': author_id,
                'doi': doi_string,
                'author_order': author_order
            }
            DOIAuthorMapping.get_or_create(**author_map_insert_item)

    @staticmethod
    def _update_doi_metadata_info(doi_info, doi_string):
        # loop through metadata entries and make doi_info entries
        for field in doi_info:
            lookup_item = {
                'key': field,
                'doi': doi_string
            }

            insert_item = {
                'value': doi_info.get(field)
            }
            item, _created = DOIInfo.get_or_create(**lookup_item, defaults=insert_item)
            if not _created and item.value != insert_item['value']:
                item.value = insert_item['value']
                item.save()

    @staticmethod
    def _update_doi_entry_info(doi_string, doi_info, creator, status='pending', released=False):
        lookup_item = {
            'doi': doi_string
        }
        insert_item = {
            'status': status,
            'released': released,
            'site_url': doi_info['site_url']
        }
        osti_elink_url_base = 'https://www.osti.gov/elink/2416api'

        if creator is not None:
            insert_item['creator'] = creator
        doi_entry, _created = DOIEntries.get_or_create(**lookup_item, defaults=insert_item)
        if not _created:
            doi_entry.status = status
            doi_entry.released = released
            doi_entry.site_url = doi_info['site_url']
            doi_entry.creator = creator
            doi_entry.save(only=doi_entry.dirty_fields)

    # CherryPy requires these named methods.
    # pylint: disable=invalid-named
    @staticmethod
    @tools.json_in()
    @tools.json_out()
    def POST():
        """Upload and create new DOI Entries."""
        items = request.json
        if not isinstance(items, (list,)) and isinstance(items, (dict, )):
            items = [items]
        new_entries_info = []
        for item in items:
            new_entry = DOIRegistrationUpdate._add_doi_record_entry(item)
            new_entries_info.append(new_entry)
            DOIRegistrationUpdate._get_updated_osti_info(
                doi_string=new_entry,
                elink_url=osti_elink_url,
                elink_user='***********',
                elink_password='************')
        return new_entries_info
