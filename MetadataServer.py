#!/usr/bin/python
"""Main metadata server script."""
from json import dumps
import cherrypy
from metadata.rest.root import Root
from metadata.orm import create_tables


def error_page_default(**kwargs):
    """The default error page should always enforce json."""
    cherrypy.response.headers['Content-Type'] = 'application/json'
    return dumps({
        'status': kwargs['status'],
        'message': kwargs['message'],
        'traceback': kwargs['traceback'],
        'version': kwargs['version']
    })


def main():
    """Main method to start the httpd server."""
    create_tables()
    cherrypy.config.update({'error_page.default': error_page_default})
    cherrypy.quickstart(Root(), '/', 'server.conf')


if __name__ == '__main__':
    main()
