#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Main metadata server script."""
import cherrypy
from metadata import CHERRYPY_CONFIG, main, error_page_default
from metadata.rest.root import Root


cherrypy.config.update({'error_page.default': error_page_default})
# pylint doesn't realize that application is actually a callable
# pylint: disable=invalid-name
application = cherrypy.Application(Root(), '/', CHERRYPY_CONFIG)
# pylint: enable=invalid-name
if __name__ == '__main__':
    main()
