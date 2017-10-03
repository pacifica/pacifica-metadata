"""CherryPy Status Metadata object class."""
import datetime
from cherrypy import tools
from dateutil.parser import parse
from peewee import Expression, OP
from metadata.rest.transaction_queries.query_base import QueryBase
from metadata.orm import Transactions, InstrumentGroup
from metadata.orm.base import db_connection_decorator
from metadata.rest.reporting_queries.detailed_transactions_list import DetailedTransactionList


class TransactionsMultiSearch(QueryBase):
    """Retrieves a list of all transactions matching the search criteria."""

    exposed = True

    @staticmethod
    def _get_transactions_from_group(instrument_group_id, proposal_id, start_time, end_time):
        # get instruments for group_id
        if instrument_group_id:
            instrument_list = TransactionsMultiSearch._get_instruments_from_group_id(
                instrument_group_id)
        else:
            instrument_list = None

        where_clause = Expression(1, OP.EQ, 1)
        # now get the appropriate transactions
        where_clause &= Transactions().where_clause(
            {'updated': start_time, 'updated_operator': 'gte'})
        where_clause &= Transactions().where_clause(
            {'updated': end_time, 'updated_operator': 'lte'})

        if instrument_list:
            where_clause &= (Transactions.instrument << instrument_list)
        if proposal_id:
            where_clause &= (Transactions.proposal == proposal_id)
        transactions_list_query = Transactions.select(Transactions.id).where(where_clause)

        transactions_list = [t['id'] for t in transactions_list_query.dicts()]
        return transactions_list

    @staticmethod
    def _get_instruments_from_group_id(group_id):
        instrument_list_query = (InstrumentGroup
                                 .select(InstrumentGroup.instrument)
                                 .where(InstrumentGroup.group == group_id).dicts())
        instrument_list = [i['instrument'] for i in instrument_list_query]
        return instrument_list

    @staticmethod
    def _get_first_last_day(month_id=None):
        today = datetime.datetime.today()
        if month_id:
            today = today.replace(month=month_id)
        first_day_of_month = today.replace(day=1).date()
        last_day_of_month = datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(days=1)
        return first_day_of_month, last_day_of_month

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    @db_connection_decorator
    def GET(**kwargs):
        """Return Transactions for a proposal_id and instrument_group_id."""
        valid_keywords = ['proposal_id', 'instrument_group_id', 'start_time', 'end_time']
        first_day_of_month, last_day_of_month = TransactionsMultiSearch._get_first_last_day()
        kwargs = {k: v for (k, v) in kwargs.items() if k in valid_keywords}

        instrument_group_id = kwargs['instrument_group_id'] if 'instrument_group_id' in kwargs else None
        proposal_id = kwargs['proposal_id'] if 'proposal_id' in kwargs else None
        start_time = parse(kwargs['start_time']) if 'start_time' in kwargs else first_day_of_month
        end_time = parse(kwargs['end_time']) if 'end_time' in kwargs else last_day_of_month

        transaction_list = TransactionsMultiSearch._get_transactions_from_group(
            instrument_group_id, proposal_id,
            start_time.strftime('%Y-%m-%d'),
            end_time.strftime('%Y-%m-%d'))

        return DetailedTransactionList.get_transaction_list_details(transaction_list)
