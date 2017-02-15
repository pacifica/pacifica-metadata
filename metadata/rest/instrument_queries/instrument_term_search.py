"""CherryPy Status Metadata object class."""
import re
import cherrypy
from cherrypy import tools
from peewee import OP, Expression
from metadata.orm import Instruments
from metadata.rest.instrument_queries.query_base import QueryBase


class InstrumentTermSearch(QueryBase):
    """InstrumentTermSearch API."""

    exposed = True

    @staticmethod
    def search_for_instrument(search_term):
        """Return a dictionary containing information about a given instrument."""
        terms = re.findall(r'[^+ ,;]+', search_term)
        keys = ['display_name', 'name_short', 'name', 'id']
        where_clause = Expression(1, OP.EQ, 1)
        for term in terms:
            term = str(term)
            where_clause_part = Expression(1, OP.EQ, 0)
            for k in keys:
                if k == 'id':
                    if re.match('[0-9]+', term):
                        where_clause_part |= Expression(
                            Instruments.id, OP.EQ, term)
                else:
                    where_clause_part |= Expression(
                        getattr(Instruments, k), OP.ILIKE, '%{0}%'.format(term))
            where_clause &= (where_clause_part)
        objs = Instruments.select().where(where_clause).order_by(Instruments.name_short)
        if len(objs) == 0:
            message = 'No instrument entries were retrieved using the terms: \''
            message += '\' and \''.join(terms) + '\''
            raise cherrypy.HTTPError('404 No Valid Instruments Located', message)

        return [QueryBase.format_instrument_block(obj) for obj in objs]

    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    def GET(search_term=None):
        """Return a set of instruments for a given user."""
        if search_term is not None and len(search_term) > 0:
            return InstrumentTermSearch.search_for_instrument(search_term)
        else:
            raise cherrypy.HTTPError(
                '400 No Search Terms Provided',
                QueryBase.compose_help_block_message()
            )
