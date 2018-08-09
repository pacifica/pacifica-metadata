#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Status Metadata object class."""
import cherrypy
from cherrypy import tools
from pacifica.metadata.orm import Transactions
from pacifica.metadata.rest.proposal_queries.query_base import QueryBase
from pacifica.metadata.orm.base import db_connection_decorator


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
            ret_hash[proposal_id] = []
            instlist = [trans.instrument for trans in Transactions.select(
                Transactions.instrument
            ).where(
                Transactions.proposal == proposal_id
            ).distinct()]
            for instrument in instlist:
                data = [x.created for x in Transactions.select(
                    Transactions.created
                ).where(
                    (Transactions.proposal == proposal_id) &
                    (Transactions.instrument == instrument)
                ).order_by(
                    Transactions.created.desc()
                ).limit(10)]
                ret_hash[proposal_id].append({
                    'instrument': instrument.id,
                    'end_time': data[0].isoformat(),
                    'start_time': data[-1].isoformat(),
                    'num_results': len(data)
                })
        return ret_hash
