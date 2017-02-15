#!/usr/bin/python
"""Test the ORM interface IngestAPI."""
from json import loads
import requests
from dateutil import parser
from cherrypy.test import helper
from test_files.loadit import main
from metadata.rest.test import CPCommonTest, DockerMetadata


class TestFileInfoAPI(CPCommonTest, helper.CPWebCase):
    """Test the ObjectInfoAPI class."""

    @classmethod
    def setup_class(cls):
        """Setup the services required by the server."""
        super(TestFileInfoAPI, cls).setup_class()
        main()

    @classmethod
    def teardown_class(cls):
        """Tear down the services required by the server."""
        super(TestFileInfoAPI, cls).teardown_class()
        DockerMetadata.stop_services()

    def _get_file_info(self, file_id_list):
        header_list = {'Content-Type': 'application/json'}
        req = requests.post(
            url='{0}/fileinfo/file_details/'.format(self.url),
            json=file_id_list,
            headers=header_list
        )
        return req

    def _get_earliest_latest(self, item_type, id_list, time_basis):
        header_list = {'Content-Type': 'application/json'}
        req = requests.post(
            url='{0}/fileinfo/earliest_latest/{1}/{2}/'.format(
                self.url, item_type, time_basis
            ),
            json=id_list,
            headers=header_list
        )
        return req

    def test_fileinfo_api(self):
        """Test the GET method."""
        # test by_user_id
        file_id_list = [103, 104]
        req = self._get_file_info(file_id_list)
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(len(req_json), 2)

    def test_bad_fileinfo_api(self):
        """Test bad file retrievals."""
        file_id_list = [105, 106]
        req = self._get_file_info(file_id_list)
        self.assertEqual(req.status_code, 404)

    def test_earliest_latest_api(self):
        """Test valid earliest/latest functionality."""
        # test for proposal single proposal by modified time
        id_list = ['1234a']
        req = self._get_earliest_latest(
            item_type='proposal',
            id_list=id_list,
            time_basis='modified'
        )
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        earliest = parser.parse(req_json['earliest'])
        latest = parser.parse(req_json['latest'])
        self.assertTrue(latest >= earliest)

        # test for proposal single proposal by modified time
        id_list = ['1234a']
        req = self._get_earliest_latest(
            item_type='proposal',
            id_list=id_list,
            time_basis='submitted'
        )
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        earliest = parser.parse(req_json['earliest'])
        latest = parser.parse(req_json['latest'])
        self.assertTrue(latest >= earliest)

    def test_bad_earliest_latest_api(self):
        """Test invalid earliest/latest functionality."""
        # test for single nonexistent proposal by modified time
        id_list = ['2345a']
        req = self._get_earliest_latest(
            item_type='proposal',
            id_list=id_list,
            time_basis='modified'
        )
        self.assertEqual(req.status_code, 404)

        # test for single existing proposal with bad item_type
        id_list = ['1234a']
        req = self._get_earliest_latest(
            item_type='bob',
            id_list=id_list,
            time_basis='modified'
        )
        self.assertEqual(req.status_code, 400)

        req = self._get_earliest_latest(
            item_type='proposal',
            id_list=id_list,
            time_basis='bob'
        )
