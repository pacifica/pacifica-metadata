#!/usr/bin/python
"""Test the ORM interface IngestAPI."""
from json import loads
import requests
from cherrypy.test import helper
from test_files.loadit import main
from metadata.rest.test import CPCommonTest, DockerMetadata


class TestFileInfoAPI(CPCommonTest, helper.CPWebCase):
    """Test the ObjectInfoAPI class."""

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

    def test_fileinfo_api(self):
        """Test the GET method."""
        main()
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
