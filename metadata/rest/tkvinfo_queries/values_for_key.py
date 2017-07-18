"""CherryPy File Details object class."""
from datetime import datetime
from cherrypy import tools
from metadata.orm import TransactionKeyValue, Keys, Values, Transactions
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
    def get_values_for_key(key, start_time, end_time):
        """Retrieve all the tkv values for a given key item."""
        # get the id of the key to look for
        val_list = (Values
                    .select(Values.value, TransactionKeyValue.transaction)
                    .join(Transactions)
                    .join(TransactionKeyValue)
                    .join(Keys)
                    .where(Keys.key == key)
                    .where(Transactions.created < end_time)
                    .where(Transactions.created >= start_time)).dicts()
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
    def GET(key, start_time=None, end_time=None):
        """Return file details for the given key/value combo."""
        key = unquote(key)
        if start_time and end_time:
            return ValuesForKey.get_values_for_key(key, datetime(start_time), datetime(end_time))
        elif start_time:
            return ValuesForKey.get_values_for_key(key, datetime(start_time), datetime.utcnow())
        elif end_time:
            return ValuesForKey.get_values_for_key(key, datetime(0), datetime(end_time))
        else:
            return ValuesForKey.get_values_for_key(key, datetime(0), datetime.utcnow())
