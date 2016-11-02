#!/usr/bin/python
"""Main metadata server script."""
from wsgiref.simple_server import make_server
import cherrypy
from metadata.rest.root import Root
from metadata.orm import create_tables

CONF = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/plain')],
    }
}
create_tables()
APP = cherrypy.Application(Root(), '/', config=CONF)
HTTPD = make_server('0.0.0.0', 8080, APP)
HTTPD.serve_forever()
