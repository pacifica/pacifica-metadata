"""CherryPy File Details object class."""
from cherrypy import tools
from peewee import DoesNotExist, fn
from urllib import quote, unquote
from metadata.orm import Files, TransactionKeyValue, Keys, Values


# pylint: disable=too-few-public-methods
class FilesWithTransactionKeyValue(object):
    """Retrieves file details for a list of files having a certain key/value combo."""

    exposed = True

    @staticmethod
    def _get_files_for_kv_pair(key, value):
        # get the id of the key to look for
        try:
            k = Keys().select(Keys.id).where(fn.Lower(Keys.key) == key.lower()).get()
        except DoesNotExist:
            # invalid keyword
            return []
        try:
            val = Values().select(Values.id).where(Values.value == value).get()
        except DoesNotExist:
            # invalid value
            return []
        tkv_where_clause = TransactionKeyValue().where_clause({'key_id': k, 'value_id': val})
        tkv_list = TransactionKeyValue().select().where(tkv_where_clause)
        transaction_list = [t.transaction_id for t in tkv_list]
        if len(transaction_list) == 0:
            # valid key, valid value, no relations
            return []

        files_query = Files().select().where(Files.transaction_id << transaction_list)

        return [f.to_hash() for f in files_query]

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    def GET(key, value):
        """Return file details for the given key/value combo."""
        key = unquote(key)
        value = unquote(value)
        return FilesWithTransactionKeyValue._get_files_for_kv_pair(key, value)
