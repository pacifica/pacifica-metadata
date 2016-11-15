#!/usr/bin/python
"""Main metadata server script."""
import cherrypy
from metadata.rest.root import Root
from metadata.orm import create_tables

create_tables()
cherrypy.quickstart(Root(), '/', 'server.conf')
