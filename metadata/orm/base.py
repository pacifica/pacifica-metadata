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
from peewee import Model, DateTimeField, Expression, OP, DoesNotExist
from cherrypy import request, HTTPError

# Primary PeeWee database connection object constant
DB = pgdb(getenv('POSTGRES_ENV_POSTGRES_DB'),
          user=getenv('POSTGRES_ENV_POSTGRES_USER'),
          password=getenv('POSTGRES_ENV_POSTGRES_PASSWORD'),
          host=getenv('POSTGRES_PORT_5432_TCP_ADDR'),
          port=getenv('POSTGRES_PORT_5432_TCP_PORT')
         )

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

    def to_hash(self):
        """
        Converts the base object fields into serializable attributes
        in a hash.
        """
        obj = {}
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
                kwargs[date] = datetime.fromtimestamp(kwargs[date])
                where_clause &= Expression(my_class.__dict__[date].field, OP.EQ, kwargs[date])
        return where_clause

    #
    # CherryPy secton of methods and attributes
    #
    exposed = True

    # CherryPy requires these named methods.
    # pylint: disable=invalid-name
    def GET(self, **kwargs):
        """
        Implements the GET HTTP method. Returns the json object based on
        fields passed into kwargs.
        """
        try:
            obj = self.get(self.where_clause(kwargs))
        except DoesNotExist, ex:
            raise HTTPError(404, str(ex))
        return obj.to_json()

    def POST(self, **kwargs):
        """
        Implements the POST HTTP method. Gets the object similar to GET()
        and uses the request body to update the object and saves it.
        """
        print "Running POST"
        try:
            obj = self.get(self.where_clause(kwargs))
        except DoesNotExist, ex:
            raise HTTPError(404, str(ex))
        try:
            obj.from_json(request.body.read())
        except ValueError, ex:
            raise HTTPError(500, str(ex))
        obj.updated = datetime.now()
        obj.save()

    def PUT(self):
        """
        Implements the PUT HTTP method. Creates an object based on the
        request body.
        """
        print "Running PUT"
        try:
            self.from_json(request.body.read())
        except ValueError, ex:
            raise HTTPError(500, str(ex))
        self.deleted = datetime.fromtimestamp(0)
        self.updated = datetime.now()
        self.created = datetime.now()
        self.save(force_insert=True)

    def DELETE(self, **kwargs):
        """
        Implements the DELETE HTTP method. Gets a single object based on
        kwargs, sets the deleted flag and saves the object.
        """
        try:
            obj = self.get(self.where_clause(kwargs))
        except DoesNotExist, ex:
            raise HTTPError(404, str(ex))
        obj.deleted = datetime.now()
        obj.save()
    # pylint: enable=invalid-name
