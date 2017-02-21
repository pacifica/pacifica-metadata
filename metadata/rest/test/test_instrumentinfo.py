#!/usr/bin/python
"""Test the ORM interface InstrumentInfo."""
import requests
from cherrypy.test import helper
from test_files.loadit import main
from metadata.rest.test import CPCommonTest, DockerMetadata


class TestObjectInfoAPI(CPCommonTest, helper.CPWebCase):
    """Test the ObjectInfoAPI class."""

    @classmethod
    def setup_class(cls):
        """Setup the services required by the server."""
        super(TestObjectInfoAPI, cls).setup_class()
        main()

    @classmethod
    def teardown_class(cls):
        """Tear down the services required by the server."""
        super(TestObjectInfoAPI, cls).teardown_class()
        DockerMetadata.stop_services()

    def _get_instrument_details(self, instrument_id):
        header_list = {'Content-Type': 'application/json'}
        url = '{0}/instrumentinfo/by_instrument_id/{1}'.format(self.url, instrument_id)
        req = requests.get(url=url, headers=header_list)
        return req

    def _search_for_instrument(self, search_term):
        header_list = {'Content-Type': 'application/json'}
        url = '{0}/instrumentinfo/search/{1}'.format(self.url, search_term)
        req = requests.get(url=url, headers=header_list)
        return req

    def test_instrumentinfo_api(self):
        """Test the GET method."""
        # test instrument lookup with good id
        instrument_id = 54
        req = self._get_instrument_details(instrument_id)
        self.assertEqual(req.status_code, 200)
        results = req.json()
        self.assertTrue('Nittany' in results['name_short'])

        # test instrument search with known valid term
        search_term = 'nittany'
        req = self._search_for_instrument(search_term)
        self.assertEqual(req.status_code, 200)

        # test instrument search with known id term
        search_term = '54'
        req = self._search_for_instrument(search_term)
        self.assertEqual(req.status_code, 200)

    def test_bad_instrumentinfo_api(self):
        """Test the GET method with bad data."""
        # test instrument lookup with nonexistant id
        instrument_id = 96
        req = self._get_instrument_details(instrument_id)
        self.assertEqual(req.status_code, 404)

        # test instrument with malformed id
        text_instrument_id = 'bob'
        req = self._get_instrument_details(text_instrument_id)
        self.assertEqual(req.status_code, 400)

        # test instrument search with known invalid term
        search_term = 'supercalifragilistic'
        req = self._search_for_instrument(search_term)
        self.assertEqual(req.status_code, 404)

        # test instrument search with known invalid term
        search_term = None
        req = self._search_for_instrument('')
        self.assertEqual(req.status_code, 400)
