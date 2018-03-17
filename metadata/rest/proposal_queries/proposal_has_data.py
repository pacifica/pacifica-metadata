#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Status Metadata object class."""
import cherrypy
from cherrypy import tools
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
        ret_hash = {}
        for proposal_id in cherrypy.request.json:
            inst_query = Transactions.select(
                Transactions.instrument
            ).where(
                Transactions.proposal == proposal_id
            ).distinct()
            ret_hash[proposal_id] = []
            for trans in inst_query:
                instrument = trans.instrument
                query = Transactions.select(
                    Transactions.created
                ).where(
                    (Transactions.proposal == proposal_id) &
                    (Transactions.instrument == instrument)
                ).order_by(
                    Transactions.created.desc()
                ).limit(10)
                data = [x for x in query]
                ret_hash[proposal_id].append({
                    'instrument': instrument.id,
                    'start_time': data[0].created.isoformat(),
                    'end_time': data[-1].created.isoformat(),
                    'num_results': len(query)
                })
        return ret_hash
