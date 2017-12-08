#!/usr/bin/python
"""Metadata Module."""
from os import getenv

CHERRYPY_CONFIG = getenv('CHERRYPY_CONFIG', 'server.conf')
