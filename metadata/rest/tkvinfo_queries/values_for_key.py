"""CherryPy File Details object class."""
from cherrypy import tools
from metadata.orm import TransactionKeyValue, Keys, Values
from metadata.orm.base import db_connection_decorator
try:
    from urllib.parse import unquote
except ImportError:
    from urlparse import unquote


# pylint: disable=too-few-public-methods
class ValuesForKey(object):
    """Retrieves a list of values for a given key from the trans_key_value table."""

    exposed = True

    @staticmethod
    def get_values_for_key(key):
        """Retrieve all the tkv values for a given key item."""
        # get the id of the key to look for
        val_list = (Values
                    .select(Values.value, TransactionKeyValue.transaction)
                    .join(TransactionKeyValue)
                    .join(Keys)
                    .where(Keys.key == key)).dicts()
        ret = {}
        for val in val_list:
            if val.get('value') not in ret:
                ret[val.get('value')] = []
            ret[val.get('value')].append(val.get('transaction'))
        return ret

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_out()
    @db_connection_decorator
    def GET(key):
        """Return file details for the given key/value combo."""
        key = unquote(key)
        return ValuesForKey.get_values_for_key(key)
