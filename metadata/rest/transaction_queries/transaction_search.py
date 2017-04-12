"""CherryPy Status Metadata object class."""
import cherrypy
# import re
from cherrypy import tools, HTTPError
from peewee import Expression, OP
from metadata.rest.transaction_queries.query_base import QueryBase
from metadata.orm import Transactions


class TransactionSearch(QueryBase):
    """Retrieves a list of all transactions matching the search criteria."""

    exposed = True

    @staticmethod
    def _search_transactions(search_terms):
        # build the search query from keyword bits
        trans = Transactions()
        where_clause = Expression(1, OP.EQ, 1)
        query = trans.select()
        for term in search_terms:
            value = str(search_terms[term]).replace('+', ' ')
            if term in ['proposal', 'proposal_id'] and value != '-1':
                where_clause &= Transactions().where_clause({'proposal': value})
                continue
            if term in ['instrument', 'instrument_id'] and value != '-1':
                where_clause &= Transactions().where_clause({'instrument': value})
                continue
            if term in ['start', 'start_time']:
                where_clause &= Transactions().where_clause(
                    {'updated': value, 'updated_operator': 'gte'})
                continue
            if term in ['end', 'end_time']:
                where_clause &= Transactions().where_clause(
                    {'updated': value, 'updated_operator': 'lte'})
                continue
            if term in ['user', 'user_id', 'person',
                        'person_id', 'submitter', 'submitter_id'] and value != '-1':
                where_clause &= Transactions().where_clause({'submitter': value})
                continue
            if term in ['transaction_id'] and value != '-1':
                where_clause &= Transactions().where_clause({'_id': value})
                continue

        query = query.where(where_clause)

        return [t.id for t in query]

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    def GET(option='details', **kwargs):
        """Return transactions for the search params."""
        option = 'details' if option not in ['list', 'details'] else option

        valid_keywords = [
            'proposal', 'proposal_id', 'instrument', 'instrument_id', 'requesting_user',
            'time_frame', 'start_time', 'start', 'end_time', 'end', 'transaction_id',
            'user', 'user_id', 'person', 'person_id', 'submitter', 'submitter_id'
        ]
        kwargs = {k: v for (k, v) in kwargs.items() if k in valid_keywords}
        if len(kwargs) == 0:
            message = 'Invalid transaction details search request. '
            cherrypy.log.error(message)
            raise HTTPError(
                '400 Invalid Request Options',
                QueryBase.compose_help_block_message()
            )
        else:
            transactions = TransactionSearch._search_transactions(kwargs)

        results = QueryBase._get_transaction_info_blocks(transactions, option)

        return results
