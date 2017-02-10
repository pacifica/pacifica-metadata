"""CherryPy Status Metadata object class."""
import re
from cherrypy import tools, HTTPError
from peewee import DoesNotExist
from metadata.orm import Proposals, Instruments, ProposalInstrument
from metadata.rest.proposal_queries.query_base import QueryBase
from metadata.orm.base import db_connection_decorator


class ProposalLookup(QueryBase):
    """Retrieves a set of proposals for a given keyword set."""

    exposed = True

    @staticmethod
    def _get_proposal_details(proposal_id):
        """Return a formatted dictionary containing the details of a given Proposal entry."""
        terms = re.findall(r'[^+ ,;]+', str(proposal_id))
        for term in terms:
            # Take the first thing that matches standard proposal id numbering
            if re.match('[0-9]+[a-z]?', term):
                proposal_id = term
                break
        try:
            proposal_entry = (Proposals.get(Proposals.id == proposal_id))
        except DoesNotExist:
            message = 'No Proposal with an ID of {0} was found'.format(
                proposal_id)
            raise HTTPError('404 Not Found', message)

        prop_inst = ProposalInstrument()
        pi_where_clause = prop_inst.where_clause(
            {'proposal_id': proposal_id})
        instrument_entries = (Instruments
                              .select(
                                  Instruments.id, Instruments.display_name,
                                  Instruments.name, Instruments.name_short,
                                  Instruments.active
                              )
                              .order_by(Instruments.id)
                              .join(ProposalInstrument)
                              .where(pi_where_clause))
        instruments = {i.id: {
            'id': i.id,
            'display_name': i.display_name,
            'name': i.name,
            'name_short': i.name_short,
            'active': i.active
        } for i in instrument_entries}

        return QueryBase.format_proposal_block(proposal_entry, instruments)

    # CherryPy requires these named methods
    # Add HEAD (basically Get without returning body
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    @db_connection_decorator
    def GET(proposal_id=None):
        """CherryPy GET method."""
        return ProposalLookup._get_proposal_details(proposal_id)
