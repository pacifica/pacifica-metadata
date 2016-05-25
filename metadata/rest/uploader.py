#!/usr/bin/python
"""
Core interface for the uploader metadata objects to interface with CherryPy
"""
from json import loads
from cherrypy import request, HTTPError
#from peewee import DoesNotExist, IntegrityError
from metadata.rest.orm import CherryPyAPI

class UploaderAPI(CherryPyAPI):
    """
    Uploader ingest API
    """
    exposed = True
    # CherryPy requires these named methods.
    # pylint: disable=invalid-name
    def PUT(self):
        try:
            json = loads(request.body.read())
        except ValueError, ex:
            raise HTTPError(500, str(ex))
        print json
