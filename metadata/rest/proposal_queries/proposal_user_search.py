"""CherryPy Status Metadata object class."""
import re
from cherrypy import tools, HTTPError
from metadata.orm import Proposals, ProposalParticipant
from metadata.rest.proposal_queries.query_base import QueryBase
from metadata.rest.userinfo import user_exists_decorator


class ProposalUserSearch(QueryBase):
    """ProposalUserSearch API."""

    exposed = True

    @staticmethod
    @user_exists_decorator
    def get_proposals_for_user(user_id):
        """Return a list of formatted proposal objects for the indicated user."""
        # get list of proposal_ids for this user
        where_clause = ProposalParticipant().where_clause(
            {'person_id': user_id})
        proposals = (Proposals
                     .select(
                         Proposals.id, Proposals.title, Proposals.actual_start_date,
                         Proposals.actual_end_date, Proposals.closed_date,
                         Proposals.accepted_date, Proposals.submitted_date
                     )
                     .join(ProposalParticipant)
                     .where(where_clause)
                     .order_by(Proposals.title))
        return [QueryBase.format_proposal_block(p) for p in proposals if p]

    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    def GET(user_id=None):
        """Return a set of proposals for a given user."""
        if user_id is not None:
            user_ids = re.findall('[0-9]+', user_id)
            if len(user_ids) > 0:
                user_id = int(user_ids.pop(0))
            else:
                raise HTTPError(
                    '400 Invalid User ID',
                    '"{0}" is not a valid user ID'.format(user_id)
                )
        else:
            raise HTTPError(
                '400 Invalid User ID',
                'No user ID specified'
            )

        return ProposalUserSearch.get_proposals_for_user(user_id)
