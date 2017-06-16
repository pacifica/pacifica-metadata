#!/usr/bin/python
"""Test the REST interfaces."""
import logging
import cherrypy
from cherrypy.test import helper
from metadata.orm import create_tables, ORM_OBJECTS
from metadata.rest.root import Root
from test_files.loadit import main
from MetadataServer import error_page_default


# pylint: disable=too-few-public-methods
class CPCommonTest(helper.CPWebCase):
    """Common test info for all rest."""

    PORT = 8121
    HOST = '127.0.0.1'
    url = 'http://{0}:{1}'.format(HOST, PORT)
    headers = {'content-type': 'application/json'}
    __test__ = False

    @classmethod
    def teardown_class(cls):
        """Tear down the services required by the server."""
        super(CPCommonTest, cls).teardown_class()
        for dbobj in ORM_OBJECTS:
            dbobj.drop_table()

    @classmethod
    def setup_class(cls):
        """Setup the services required by the server."""
        super(CPCommonTest, cls).setup_class()
        main()

    @staticmethod
    def setup_server():
        """Start all the services."""
        logger = logging.getLogger('urllib2')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler())
        create_tables()
        cherrypy.config.update({'error_page.default': error_page_default})
        cherrypy.config.update('server.conf')
        cherrypy.tree.mount(Root(), '/', 'server.conf')
# pylint: enable=too-few-public-methods
