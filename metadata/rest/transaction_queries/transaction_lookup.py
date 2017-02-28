"""CherryPy Status Transaction Metadata object class."""
import re
import cherrypy
from cherrypy import tools, HTTPError
from metadata.rest.transaction_queries.query_base import QueryBase


class TransactionLookup(QueryBase):
    """Retrieves details for an individual transaction."""

    exposed = True

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    def GET(trans_id=None):
        """Return details about the specified transaction entity."""
        if trans_id is not None and re.match('[0-9]+', trans_id):
            cherrypy.log.error('transaction details request')
            return QueryBase._get_transaction_info_block(trans_id)
        else:
            message = 'Invalid transaction details lookup request. '
            message += "'{0}' is not a valid transaction_id".format(
                trans_id)
            cherrypy.log.error(message)
            raise HTTPError(
                '400 Invalid Transaction ID',
                QueryBase.compose_help_block_message()
            )
