#!/usr/bin/python
"""Metadata Module."""
from os import getenv
import cherrypy
from metadata.rest.root import Root
from metadata.orm import create_tables


CHERRYPY_CONFIG = getenv('CHERRYPY_CONFIG', 'server.conf')


def main():
    """Main method to start the httpd server."""
    create_tables()
    cherrypy.quickstart(Root(), '/', CHERRYPY_CONFIG)
