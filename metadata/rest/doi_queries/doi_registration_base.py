#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy DOI Registration Updater object class."""
from __future__ import print_function
from metadata.orm import DOIEntries, DOIInfo
from metadata.orm.utils import datetime_now_nomicrosecond

# pylint: disable=too-few-public-methods


class DOIRegistrationBase(object):
    """Base class for DOI registration functionality."""

    @staticmethod
    def change_doi_entry_info(doi_string, doi_info, creator, status='pending', released=False):
        """Update or create DOI entries."""
        lookup_item = {
            'doi': doi_string
        }
        insert_item = {
            'status': status,
            'released': released,
            'site_url': doi_info['site_url']
        }
        if creator is not None:
            insert_item['creator_id'] = creator
        doi_entry, _created = DOIEntries.get_or_create(
            **lookup_item, defaults=insert_item)
        if not _created:
            doi_entry.from_hash(insert_item)
            doi_entry.updated = datetime_now_nomicrosecond()
            doi_entry.save(only=doi_entry.dirty_fields)

        DOIRegistrationBase._update_doi_metadata_info(doi_info, doi_string)

        return doi_entry, _created

    @staticmethod
    def _update_doi_metadata_info(doi_info, doi_string):
        # loop through metadata entries and make doi_info entries
        for md_field in doi_info:
            if doi_info[md_field] is None:
                continue
            lookup_item = {
                'key': md_field,
                'doi': doi_string
            }
            insert_item = {}
            insert_item['value'] = doi_info.get(md_field)
            item, _created = DOIInfo.get_or_create(
                **lookup_item, defaults=insert_item)
            if not _created and item.value != insert_item['value']:
                item.value = insert_item['value']
                item.save()
