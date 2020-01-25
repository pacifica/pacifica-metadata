#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Status Metadata object class."""
from cherrypy import tools, HTTPError
from collections import defaultdict
from peewee import fn
from pacifica.metadata.rest.reporting_queries.query_base import QueryBase
from pacifica.metadata.orm import TransSIP
from pacifica.metadata.orm.base import db_connection_decorator
from pacifica.metadata.rest.reporting_queries.summarize_by_date import SummarizeByDate


# pylint: disable=too-few-public-methods
class TransactionReporting(QueryBase):
    """Retrieves a list of all transactions matching the search criteria."""

    exposed = True

    @staticmethod
    def get_transaction_date_range_details(start_date, end_date):
        """Return a transaction set grouped on instrument and project for a given time span."""
        # pylint: disable=no-member
        transaction_query = (
            TransSIP().select(
                fn.Count(TransSIP.id).alias('transaction_count'),
                fn.Min(TransSIP.updated).alias('earliest_upload_date'),
                fn.Max(TransSIP.updated).alias('latest_upload_date'),
                fn.Min(TransSIP.submitter).alias('uploaded_by_id'),
                TransSIP.project.alias('project_id'),
                TransSIP.instrument.alias('instrument_id')
            )
            .group_by(TransSIP.project, TransSIP.instrument)
            .having(fn.Min(TransSIP.updated) >= start_date)
            .having(fn.Max(TransSIP.updated) <= end_date)
        )
        # pylint: enable=no-member
        transaction_results = defaultdict(dict)

        for rec in transaction_query.dicts():
            transaction_results[rec['project_id']][rec['instrument_id']] = {
                'transaction_count': int(rec['transaction_count']),
                'upload_date_start': SummarizeByDate.utc_to_local(
                    rec['earliest_upload_date']).date().strftime('%Y-%m-%d'),
                'upload_date_end': SummarizeByDate.utc_to_local(
                    rec['latest_upload_date']).date().strftime('%Y-%m-%d'),
                'project_id': rec['project_id'],
                'instrument_id': rec['instrument_id'],
                'uploaded_by_id': rec['uploaded_by_id']
            }

        return transaction_results

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    @db_connection_decorator
    def GET(start_date=None, end_date=None):
        """Return a transaction summary for a given date range."""
        if start_date is None:
            raise HTTPError(
                '400 Invalid Start Date',
                'No starting date specified'
            )

        if end_date is None:
            raise HTTPError(
                '400 Invalid End Date',
                'No ending date specified'
            )

        return TransactionReporting.get_transaction_date_range_details(start_date, end_date)
