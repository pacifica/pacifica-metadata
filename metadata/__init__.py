#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Metadata Module."""
from time import sleep
from threading import Thread
from os import getenv
from json import dumps
from argparse import ArgumentParser, SUPPRESS
import cherrypy
from metadata.rest.root import Root
from metadata.orm import create_tables


CHERRYPY_CONFIG = getenv('CHERRYPY_CONFIG', 'server.conf')


def error_page_default(**kwargs):
    """The default error page should always enforce json."""
    cherrypy.response.headers['Content-Type'] = 'application/json'
    return dumps({
        'status': kwargs['status'],
        'message': kwargs['message'],
        'traceback': kwargs['traceback'],
        'version': kwargs['version']
    })


def stop_later(doit=False):
    """Used for unit testing stop after 10 seconds."""
    if not doit:
        return

    def sleep_then_exit():
        """sleep for 10 seconds then call cherrypy exit."""
        sleep(10)
        cherrypy.engine.exit()
    sleep_thread = Thread(target=sleep_then_exit)
    sleep_thread.daemon = True
    sleep_thread.start()


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
    parser.add_argument('--stop-after-a-moment', help=SUPPRESS,
                        default=False, dest='stop_later',
                        action='store_true')
    args = parser.parse_args()
    create_tables()

    stop_later(args.stop_later)

    cherrypy.config.update({'error_page.default': error_page_default})
    cherrypy.config.update({
        'server.socket_host': args.address,
        'server.socket_port': args.port
    })
    cherrypy.quickstart(Root(), '/', args.config)
