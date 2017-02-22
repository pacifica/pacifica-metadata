"""CherryPy Status Metadata object class."""
import cherrypy
from cherrypy import tools
from metadata.orm import Instruments, ProposalParticipant, ProposalInstrument
from metadata.rest.instrument_queries.query_base import QueryBase
from metadata.orm.base import db_connection_decorator
from metadata.rest.userinfo import user_exists_decorator


class InstrumentUserSearch(QueryBase):
    """InstrumentUserSearch API."""

    exposed = True

    @staticmethod
    @user_exists_decorator
    def get_instruments_for_user(user_id):
        """Return a list of formatted instrument objects for the indicated user."""
        where_clause = ProposalParticipant().where_clause(
            {'person_id': user_id})

        instrument_list = (Instruments
                           .select()
                           .distinct()
                           .join(ProposalInstrument,
                                 on=(ProposalInstrument.instrument == Instruments.id))
                           .join(ProposalParticipant,
                                 on=(ProposalParticipant.proposal == ProposalInstrument.proposal))
                           .where(where_clause))
        if len(instrument_list) == 0:
            message = 'No instrument entries were retrieved the requested user'
            raise cherrypy.HTTPError(
                '404 No Valid Instruments Located', message)

        return [QueryBase.format_instrument_block(obj) for obj in instrument_list]

    # pylint: disable=invalid-name
    # pylint: disable=duplicate-code
    @staticmethod
    @tools.json_out()
    @db_connection_decorator
    def GET(user_id):
        """Return a set of instruments for a given user."""
        inst_list = InstrumentUserSearch.get_instruments_for_user(user_id=user_id)
        return inst_list
