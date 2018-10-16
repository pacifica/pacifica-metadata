#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Status Metadata object class."""
import re
import cherrypy
from cherrypy import tools
from peewee import OP, Expression
from pacifica.metadata.orm import Proposals
from pacifica.metadata.rest.proposal_queries.query_base import QueryBase
from pacifica.metadata.orm.base import db_connection_decorator


class ProposalTermSearch(QueryBase):
    """ProposalTermSearch API."""

    exposed = True

    @staticmethod
    def search_for_proposal(search_term):
        """Return a dictionary containing information about a given proposal."""
        terms = re.findall(r'[^+ ,;]+', search_term)
        keys = ['title', 'id']
        where_clause = Expression(1, OP.EQ, 1)
        for term in terms:
            term = str(term)
            where_clause_part = Expression(1, OP.EQ, 0)
            for k in keys:
                if k == 'id':
                    if re.match('[0-9]+[a-z]?', term):
                        where_clause_part |= (
                            Proposals.id == term
                        )
                        where_clause_part |= (
                            Proposals.id.contains(term)
                        )
                else:
                    where_clause_part |= (
                        getattr(Proposals, k).contains(term)
                    )
            where_clause &= (where_clause_part)
        objs = Proposals.select().where(where_clause).order_by(Proposals.title)
        if not objs:
            message = 'No proposal entries were retrieved using the terms: \''
            message += '\' and \''.join(terms) + '\''
            raise cherrypy.HTTPError('404 No Valid Proposals Located', message)

        return [QueryBase.format_proposal_block(obj) for obj in objs]

    # pylint: disable=invalid-name
    # pylint: disable=duplicate-code
    @staticmethod
    @tools.json_out()
    @db_connection_decorator
    def GET(search_term=None):
        """Return a set of proposals for a given user."""
        if search_term is not None:
            return ProposalTermSearch.search_for_proposal(search_term)
        else:
            raise cherrypy.HTTPError(
                '400 No Search Terms Provided',
                QueryBase.proposal_help_block_message()
            )
