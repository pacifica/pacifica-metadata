#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Status Metadata object class."""
from cherrypy import tools, request
from dateutil import parser
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
        query = (
            TransSip().select(
                fn.Count(TransSip.id).alias('transaction_count'),
                fn.Min(TransSIP.updated).alias('earliest_upload_date'),
                fn.Max(TransSIP.updated).alias('latest_upload_date'),
                fn.Min(TransSip.submitter).alias('uploaded_by_id'),
                TransSip.project.alias('project_id'),
                TransSip.instrument.alias('instrument_id')
            )
            .group_by(TransSip.project, TransSip.instrument)
            .having(fn.Min(TransSip.updated >= start_date))
            .having(fn.Max(TransSip.updated <= end_date))
        )
        # pylint: enable=no-member
        return [
            {
                'transaction_count': int(r['transaction_count']),
                'upload_date_start': SummarizeByDate.utc_to_local(r['earliest_upload_date']).date().strftime('%Y-%m-%d'),
                'upload_date_end': SummarizeByDate.utc_to_local(r['latest_upload_date']).date().strftime('%Y-%m-%d'),
                'project_id': r['project_id'],
                'instrument_id': r['instrument_id'],
                'uploaded_by_id': r['uploaded_by_id']
            } for r in query.dicts()
        ]

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_in()
    @tools.json_out()
    @db_connection_decorator
    def GET(start_date=None, end_date=None):
        """Return a transaction summary for a given date range."""
        if start_date is not None:
            start = parser.parse(start_date)
        else:
            raise HTTPError(
                '400 Invalid Start Date',
                'No starting date specified'
            )

        if end_date is not None:
            end = parser.parse(end_date)
        else:
            raise HTTPError(
                '400 Invalid End Date',
                'No ending date specified'
            )

        return TransactionReporting.get_transaction_date_range_details(start_date, end_date)
