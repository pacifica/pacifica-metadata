#!/usr/bin/python
"""Test the ORM interface ElasticUpdateAPI."""
from json import loads
import requests
from dateutil import parser
from metadata.rest.test import CPCommonTest


class TestElasticUpdateAPI(CPCommonTest):
    """Test the ElasticUpdateAPI class."""

    __test__ = True

    def _post_to_elasticupdate_api(self, object_name, id_list):
        header_list = {'Content-Type': 'application/json'}
        req = requests.post(
            url='{0}/elasticupdate/{1}'.format(
                self.url, object_name
            ),
            json=id_list,
            headers=header_list
        )
        return req

    def test_elasticupdate_api(self):
        """Test the POST method."""
        orm_object_list = ['instruments']
        id_list = []
        for object_name in orm_object_list:
            req = self._post_to_elasticupdate_api(object_name, id_list)
            self.assertEqual(req.status_code, 200)
            id_list = [54]
            req = self._post_to_elasticupdate_api(object_name, id_list)
            self.assertEqual(req.status_code, 200)
