"""CherryPy Status Metadata object class."""
from cherrypy import tools, request
from peewee import fn
from metadata.rest.reporting_queries.query_base import QueryBase
from metadata.orm import Transactions, Files


# pylint: disable=too-few-public-methods
class DetailedTransactionList(QueryBase):
    """Retrieves a list of all transactions matching the search criteria."""

    exposed = True

    @staticmethod
    def _get_transaction_list_details(transaction_list):
        query = (Files().select(
            Files.transaction.alias('upload_id'),
            fn.Max(Transactions.updated).alias('upload_date'),
            fn.Min(Files.mtime).alias('file_date_start'),
            fn.Max(Files.mtime).alias('file_date_end'),
            fn.Min(Transactions.submitter).alias('uploaded_by_id'),
            fn.Sum(Files.size).alias('bundle_size'),
            fn.Count(Files.id).alias('file_count'),
            fn.Min(Transactions.updated).alias('upload_datetime'))
                 .join(Transactions)
                 .where(Files.transaction << transaction_list)
                 .group_by(Files.transaction))
        print query.sql()

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_in()
    @tools.json_out()
    def POST():
        """Return summaryinfo for a given object type/id/time range combo."""
        # parse object list
        transaction_list = request.json

        return DetailedTransactionList._get_transaction_list_details(transaction_list)
