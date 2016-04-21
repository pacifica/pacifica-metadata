#!/usr/bin/python
"""
Core interface for each ORM object to interface with CherryPy
"""
from datetime import datetime
from cherrypy import request, HTTPError
from peewee import DoesNotExist
from metadata.orm.base import PacificaModel
from metadata.elastic.orm import ElasticAPI

class CherryPyAPI(PacificaModel, ElasticAPI):
    """
    Core CherryPy interface for all orm objects
    """
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
