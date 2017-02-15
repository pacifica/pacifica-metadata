#!/usr/bin/python
"""Test the ORM interface IngestAPI."""
from json import loads
import requests
from cherrypy.test import helper
from test_files.loadit import main
from metadata.rest.test import CPCommonTest, DockerMetadata


class TestProposalInfoAPI(CPCommonTest, helper.CPWebCase):
    """Test the ObjectInfoAPI class."""

    @classmethod
    def setup_class(cls):
        """Setup the services required by the server."""
        super(TestProposalInfoAPI, cls).setup_class()
        main()

    @classmethod
    def teardown_class(cls):
        """Tear down the services required by the server."""
        super(TestProposalInfoAPI, cls).teardown_class()
        DockerMetadata.stop_services()

    def test_proposalinfo_api(self):
        """Test the GET method."""
        # test by_user_id
        user_id = 10
        req = requests.get(
            '{0}/proposalinfo/by_user_id/{1}'.format(self.url, user_id))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(len(req_json), 1)

        # test individual lookup
        proposal_id = '1234a'
        req = requests.get(
            '{0}/proposalinfo/by_proposal_id/{1}'.format(self.url, proposal_id))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(req_json['id'], proposal_id)

        # test proposal search
        search_terms = 'pac+devel'
        req = requests.get(
            '{0}/proposalinfo/search/{1}'.format(self.url, search_terms))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertTrue(len(req_json) >= 1)
        # obj = req_json.pop()
        # self.assertEqual(obj['id'], proposal_id)

        search_terms = '1234a'
        req = requests.get(
            '{0}/proposalinfo/search/{1}'.format(self.url, search_terms))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(len(req_json), 1)
        obj = req_json.pop()
        self.assertEqual(obj['id'], proposal_id)

    def test_bad_proposalinfo_api(self):
        """Test the GET method with bad data."""
        str_user_id = 'bob'
        req = requests.get(
            '{0}/proposalinfo/by_user_id/{1}'.format(self.url, str_user_id))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('"bob" is not a valid user ID' in req.text)
        req = requests.get('{0}/proposalinfo/by_user_id'.format(self.url))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('No user ID specified' in req.text)
        user_id = 11
        req = requests.get(
            '{0}/proposalinfo/by_user_id/{1}'.format(self.url, user_id))
        self.assertEqual(req.status_code, 404)

        proposal_id = 'my_proposal'
        req = requests.get(
            '{0}/proposalinfo/by_proposal_id/{1}'.format(self.url, proposal_id))
        self.assertEqual(req.status_code, 404)
        self.assertTrue(
            'No Proposal with an ID of my_proposal was found' in req.text)
        proposal_id = '2345b'
        req = requests.get(
            '{0}/proposalinfo/by_proposal_id/{1}'.format(self.url, proposal_id))
        self.assertEqual(req.status_code, 404)
        self.assertTrue(
            'No Proposal with an ID of 2345b was found' in req.text)

        req = requests.get('{0}/proposalinfo/by_proposal_id'.format(self.url))
        self.assertEqual(req.status_code, 404)
        self.assertTrue('No Proposal with an ID of None was found' in req.text)

        search_terms = ''
        req = requests.get(
            '{0}/proposalinfo/search'.format(self.url))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('No Search Terms Provided' in req.text)

        search_terms = 'bob+uncle'
        req = requests.get(
            '{0}/proposalinfo/search/{1}'.format(self.url, search_terms))
        self.assertEqual(req.status_code, 404)
        self.assertTrue('No Valid Proposals' in req.text)
