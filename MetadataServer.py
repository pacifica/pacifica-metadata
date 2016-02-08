#!/usr/bin/python

import cherrypy
from wsgiref.simple_server import make_server
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
application = cherrypy.Application(Root(), '/', config=CONF)
HTTPD = make_server('0.0.0.0', 8051, application)
HTTPD.serve_forever()
