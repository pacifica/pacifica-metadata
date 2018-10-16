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
    def make_doi_entry_info(doi_string, doi_info, creator, status='pending', released=False):
        """Update or create DOI entries."""
        lookup_item = {
            'doi': doi_string
        }
        insert_item = {
            'status': status,
            'released': released,
            'site_url': doi_info['site_url'],
            'creator': creator
        }
        doi_entry, _created = DOIEntries.get_or_create(
            **lookup_item, defaults=insert_item)

        DOIRegistrationBase._update_doi_metadata_info(doi_info, doi_string)

        return doi_entry, _created

    @staticmethod
    def change_doi_entry_info(doi_string, doi_info, status='pending', released=False):
        """Update or create DOI entries."""
        doi_entry = DOIEntries.get(DOIEntries.doi == doi_string)
        insert_item = {
            'status': status,
            'released': released,
            'site_url': doi_info['site_url']
        }
        doi_entry.from_hash(insert_item)
        doi_entry.updated = datetime_now_nomicrosecond()
        doi_entry.save(only=doi_entry.dirty_fields)

        DOIRegistrationBase._update_doi_metadata_info(doi_info, doi_string)

        return doi_entry

    @staticmethod
    def _update_doi_metadata_info(doi_info, doi_string):
        # loop through metadata entries and make doi_info entries
        doi_info.pop('authors', None)
        info = (md_field for md_field in doi_info if doi_info[md_field])
        for md_field in info:
            val = doi_info.get(md_field)
            if isinstance(val, list):
                val = ', '.join(val)
            item, _created = DOIInfo.get_or_create(
                key=md_field, doi=doi_string,
                defaults={'value': val}
            )
            item.value = val
            item.save(only=item.dirty_fields)
