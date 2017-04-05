"""CherryPy Status Transaction Metadata object class."""
from cherrypy import tools
from peewee import fn
from metadata.rest.transaction_queries.query_base import QueryBase
from metadata.orm import Transactions

# pylint: disable=too-few-public-methods


class TransactionLast(QueryBase):
    """Retrieves details for an individual transaction."""

    exposed = True

    @staticmethod
    def _get_last_known_transaction():
        txn_id = (Transactions
                  .select(fn.Max(Transactions.id))
                  .where(Transactions.deleted >> None)
                  .dicts()
                  .get())
        return {'latest_transaction_id': txn_id['id']}

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    def GET():
        """Return details about the specified transaction entity."""
        return TransactionLast._get_last_known_transaction()
