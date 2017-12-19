#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Metadata Module."""
from os import getenv
from argparse import ArgumentParser
import cherrypy
from metadata.rest.root import Root
from metadata.orm import create_tables


CHERRYPY_CONFIG = getenv('CHERRYPY_CONFIG', 'server.conf')


def main():
    """Main method to start the httpd server."""
    parser = ArgumentParser(description='Run the metadata server.')
    parser.add_argument('-c', '--config', metavar='CONFIG', type=str,
                        default=CHERRYPY_CONFIG, dest='config',
                        help='cherrypy config file')
    parser.add_argument('-p', '--port', metavar='PORT', type=int,
                        default=8121, dest='port',
                        help='port to listen on')
    parser.add_argument('-a', '--address', metavar='ADDRESS',
                        default='localhost', dest='address',
                        help='address to listen on')
    args = parser.parse_args()
    create_tables()

    cherrypy.config.update({
        'server.socket_host': args.address,
        'server.socket_port': args.port
    })
    cherrypy.quickstart(Root(), '/', args.config)
