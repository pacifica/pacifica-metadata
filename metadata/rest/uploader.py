#!/usr/bin/python
"""Core interface for the uploader metadata objects to interface with CherryPy."""
from __future__ import print_function
from json import loads
from cherrypy import request, HTTPError
from metadata.rest.orm import CherryPyAPI


class UploaderAPI(CherryPyAPI):
    """Uploader ingest API."""

    exposed = True

    # CherryPy requires these named methods.
    # pylint: disable=invalid-name
    def PUT(self):
        """Sample doc string to put data to the server."""
        try:
            json = loads(request.body.read())
        except ValueError as ex:
            raise HTTPError(500, str(ex))
        print(json)
