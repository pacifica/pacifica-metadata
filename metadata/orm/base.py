#!/usr/bin/python
"""
Pacifica Metadata ORM Base Class

This class implements the basic functionality needed for all
metadata objects in the metadata model for Pacifica.
"""
from datetime import datetime
from time import mktime
from os import getenv
from json import dumps, loads

from peewee import PostgresqlDatabase as pgdb
from peewee import Model, DateTimeField, Expression, OP

# Primary PeeWee database connection object constant
DB = pgdb(getenv('POSTGRES_ENV_POSTGRES_DB'),
          user=getenv('POSTGRES_ENV_POSTGRES_USER'),
          password=getenv('POSTGRES_ENV_POSTGRES_PASSWORD'),
          host=getenv('POSTGRES_PORT_5432_TCP_ADDR'),
          port=getenv('POSTGRES_PORT_5432_TCP_PORT')
         )

DEFAULT_ELASTIC_ENDPOINT = getenv('ELASTICDB_PORT', 'tcp://127.0.0.1:9200').replace('tcp', 'http')
ELASTIC_ENDPOINT = getenv('ELASTIC_ENDPOINT', DEFAULT_ELASTIC_ENDPOINT)

"""
PacificaModel

Base class inherits from the PeeWee ORM Model class to create
required fields by all objects and serialization methods for
the base fields.

There are also CherryPy methods for creating, updating, getting
and deleting these objects in from a web service layer.
"""
class PacificaModel(Model):
    """
    Basic fields for an object within the model
    """
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)
    deleted = DateTimeField(default=datetime.now)
    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        PeeWee meta class contains the db connection.
        """
        database = DB
    # pylint: enable=too-few-public-methods

    def _rollback(self):
        """
        Reconnect to the database on errors.
        """
        self._meta.database.rollback()

    def to_hash(self):
        """
        Converts the base object fields into serializable attributes
        in a hash.
        """
        obj = {}
        obj['_type'] = self.__class__.__name__.lower()
        obj['created'] = int(mktime(self.created.timetuple()))
        obj['updated'] = int(mktime(self.updated.timetuple()))
        obj['deleted'] = int(mktime(self.deleted.timetuple()))
        return obj

    def from_hash(self, obj):
        """
        Converts the hash objects into object fields if they are
        present.
        """
        if 'created' in obj:
            self.created = datetime.fromtimestamp(int(obj['created']))
        if 'updated' in obj:
            self.updated = datetime.fromtimestamp(int(obj['updated']))
        if 'deleted' in obj:
            self.deleted = datetime.fromtimestamp(int(obj['deleted']))

    def from_json(self, json_str):
        """
        Converts the json string into the current object.
        """
        self.from_hash(loads(json_str))

    def to_json(self):
        """
        Converts the object into a json object.
        """
        return dumps(self.to_hash())

    def where_clause(self, kwargs):
        """
        PeeWee specific extension meant to be passed to a PeeWee get
        or select.
        """
        my_class = self.__class__
        where_clause = Expression(1, OP.EQ, 1)
        for date in ['deleted', 'updated', 'created']:
            if date in kwargs:
                date_obj = datetime.fromtimestamp(kwargs[date])
                where_clause &= Expression(getattr(my_class, date), OP.EQ, date_obj)
        return where_clause
