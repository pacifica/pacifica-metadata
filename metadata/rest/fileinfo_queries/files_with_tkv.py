"""CherryPy File Details object class."""
from cherrypy import tools
from peewee import DoesNotExist, fn
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
            # raise HTTPError('400 Invalid Keyword')
            return []
        try:
            val = Values().select(Values.id).where(Values.value == value).get()
        except DoesNotExist:
            # message = 'The Key/Value pair "{0}:{1}" was not found'.format(key, value)
            # raise HTTPError('404 Not Found', message)
            return []
        tkv_where_clause = TransactionKeyValue().where_clause({'key_id': k, 'value_id': val})
        try:
            tkv_list = TransactionKeyValue().select().where(tkv_where_clause)
            transaction_list = [t.transaction_id for t in tkv_list]
        except DoesNotExist:
            # raise HTTPError('404 Not Found')
            return []
        try:
            files_query = Files().select().where(Files.transaction_id << transaction_list)
        except DoesNotExist:
            # raise HTTPError('404 No Files Available')
            return []

        return [f.to_hash() for f in files_query]

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    def GET(key, value):
        """Return file details for the given key/value combo."""
        return FilesWithTransactionKeyValue._get_files_for_kv_pair(key, value)
