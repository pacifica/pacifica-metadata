#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the REST interfaces."""
import cherrypy
from cherrypy.test import helper
from pacifica.metadata.orm import ORM_OBJECTS
from pacifica.metadata.orm.sync import OrmSync, DB
from pacifica.metadata.rest.root import Root, error_page_default
from pacifica.metadata.globals import CHERRYPY_CONFIG
from test_files.loadit_test import main


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
            dbobj.drop_table(cascade=True)
        if not DB.is_closed():
            DB.close()

    @classmethod
    def setup_class(cls):
        """Setup the services required by the server."""
        super(CPCommonTest, cls).setup_class()
        main()

    @staticmethod
    def setup_server():
        """Start all the services."""
        ########
        # Uncomment the following four lines to get logging
        # import logging
        # logger = logging.getLogger('urllib2')
        # logger.setLevel(logging.DEBUG)
        # logger.addHandler(logging.StreamHandler())
        ########
        OrmSync.create_tables()
        cherrypy.config.update({'error_page.default': error_page_default})
        cherrypy.config.update(CHERRYPY_CONFIG)
        cherrypy.tree.mount(Root(), '/', CHERRYPY_CONFIG)
# pylint: enable=too-few-public-methods
