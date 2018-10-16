#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the ORM interface IngestAPI."""
from json import loads
import requests
from . import CPCommonTest


class TestProposalInfoAPI(CPCommonTest):
    """Test the ObjectInfoAPI class."""

    __test__ = True

    def test_proposalinfo_by_user_id(self):
        """Test the GET method."""
        user_id = 10
        req = requests.get(
            '{0}/proposalinfo/by_user_id/{1}'.format(self.url, user_id))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(len(req_json), 2)

    def test_proposalinfo_by_id(self):
        """Test the GET method."""
        proposal_id = '1234a'
        req = requests.get(
            '{0}/proposalinfo/by_proposal_id/{1}'.format(self.url, proposal_id))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(req_json['id'], proposal_id)

    def test_proposalinfo_search(self):
        """Test the GET method."""
        search_terms = u'pac+d\u00e9vel'
        req = requests.get(
            u'{0}/proposalinfo/search/{1}'.format(self.url, search_terms))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertTrue(len(req_json) >= 1)

    def test_proposalinfo_search_id(self):
        """Test the GET method."""
        search_terms_string = '1234a'
        proposal_id = '1234a'
        req = requests.get(
            '{0}/proposalinfo/search/{1}'.format(self.url, search_terms_string))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(len(req_json), 1)
        obj = req_json.pop()
        self.assertEqual(obj['id'], proposal_id)

    def test_proposalinfo_no_user(self):
        """Test the GET method with bad data."""
        str_user_id = 'bob'
        req = requests.get(
            '{0}/proposalinfo/by_user_id/{1}'.format(self.url, str_user_id))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('not a valid user ID' in req.text)

    def test_proposalinfo_uid_root(self):
        """Test the GET method with bad data."""
        req = requests.get('{0}/proposalinfo/by_user_id'.format(self.url))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('No user ID specified' in req.text)

    def test_proposalinfo_no_userid(self):
        """Test the GET method with bad data."""
        user_id = 21
        req = requests.get(
            '{0}/proposalinfo/by_user_id/{1}'.format(self.url, user_id))
        self.assertEqual(req.status_code, 404)

    def test_proposalinfo_no_proposal(self):
        """Test the GET method with bad data."""
        proposal_id = 'my_proposal'
        req = requests.get(
            '{0}/proposalinfo/by_proposal_id/{1}'.format(self.url, proposal_id))
        self.assertEqual(req.status_code, 400)

    def test_proposalinfo_no_proposalid(self):
        """Test the GET method with bad data."""
        proposal_id = '2345b'
        req = requests.get(
            '{0}/proposalinfo/by_proposal_id/{1}'.format(self.url, proposal_id))
        self.assertEqual(req.status_code, 404)
        self.assertTrue(
            'No Proposal with an ID of 2345b was found' in req.text)

    def test_proposalinfo_pid_root(self):
        """Test the GET method with bad data."""
        req = requests.get('{0}/proposalinfo/by_proposal_id'.format(self.url))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('Invalid Request' in req.text)

    def test_proposalinfo_no_search(self):
        """Test the GET method with bad data."""
        req = requests.get(
            '{0}/proposalinfo/search'.format(self.url))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('No Search Terms Provided' in req.text)

    def test_proposalinfo_search_not(self):
        """Test the GET method with bad data."""
        search_terms = 'bob+uncle'
        req = requests.get(
            '{0}/proposalinfo/search/{1}'.format(self.url, search_terms))
        self.assertEqual(req.status_code, 404)
        self.assertTrue('No Valid Proposals' in req.text)

    def test_has_data(self):
        """Test the proposal has data definition."""
        req = requests.post(
            '{0}/proposalinfo/has_data'.format(self.url),
            json=['1234a']
        )
        self.assertEqual(req.status_code, 200)
        self.assertTrue('1234a' in req.json())
        self.assertEqual(len(req.json()['1234a']), 1)
