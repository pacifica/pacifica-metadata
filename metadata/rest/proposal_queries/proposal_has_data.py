#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Status Metadata object class."""
import cherrypy
from cherrypy import tools
from peewee import fn
from metadata.orm import Transactions
from metadata.rest.proposal_queries.query_base import QueryBase
from metadata.orm.base import db_connection_decorator


class ProposalHasData(QueryBase):
    """Does the proposal have data for instruments."""

    exposed = True

    # CherryPy requires these named methods
    # Add HEAD (basically Get without returning body
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    @tools.json_in()
    @db_connection_decorator
    def POST():
        """CherryPy GET method."""
        return {
            proposal_id: [
                {
                    'instrument': tx.instrument.id,
                    'start_time': tx.start_time.isoformat(),
                    'end_time': tx.end_time.isoformat(),
                    'num_results': tx.count
                } for tx in Transactions.select(
                    Transactions.instrument,
                    fn.Max(Transactions.created).alias('start_time'),
                    fn.Min(Transactions.created).alias('end_time'),
                    fn.count(Transactions.id).alias('count')
                ).where(
                    Transactions.proposal == proposal_id
                ).group_by(
                    Transactions.instrument,
                    Transactions.created
                ).order_by(
                    Transactions.created
                ).limit(10)
            ] for proposal_id in cherrypy.request.json
        }
