#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy DOI Registration Updater object class."""
from __future__ import print_function
from cherrypy import tools, request, HTTPError
from dateutil.parser import parse
from pacifica.metadata.orm.utils import datetime_now_nomicrosecond
from pacifica.metadata.rest.doi_queries.doi_registration_base import DOIRegistrationBase
from pacifica.metadata.orm import DOIEntries
from pacifica.metadata.orm.base import DB

# pylint: disable=too-few-public-methods


class DOIModifiedTimeUpdate(DOIRegistrationBase):
    """Updates DOI Entries with new mod times."""

    exposed = True

    @staticmethod
    def _check_for_doi_entry(doi_string):
        check_query = DOIEntries.select().where(DOIEntries.doi == doi_string)
        return check_query.count() > 0

    @staticmethod
    def _update_modification_times(doi_list):
        """Touch a list of DOI Entries to force a modification time update."""
        touch_query = DOIEntries.select().where(DOIEntries.doi << doi_list)
        print(touch_query)
        update_count = 0
        with DB.atomic():
            for entry in touch_query:
                entry.updated = datetime_now_nomicrosecond()
                entry.save(only=entry.dirty_fields)
                update_count += 1
        return update_count

    # CherryPy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    @tools.json_in()
    def POST():
        """Update existing DOI Entries."""
        valid_content_types = ['application/json', 'text/json']
        headers = request.headers
        if headers['Content-type'] not in valid_content_types:
            raise HTTPError(415, 'Expected an entity of content type %s' %
                            ', '.join(valid_content_types))

        doi_list = request.json
        update_count = DOIModifiedTimeUpdate._update_modification_times(doi_list)

        return {'num_records_updated': update_count}
