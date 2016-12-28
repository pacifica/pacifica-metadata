#!/usr/bin/python
"""Test the ORM interface TransactionInfo."""
from json import loads
import datetime
import requests
from cherrypy.test import helper
from test_files.loadit import main
from metadata.rest.test import CPCommonTest, DockerMetadata


class TestTransactionInfoAPI(CPCommonTest, helper.CPWebCase):
    """Test the TransactionInfoAPI class."""

    @classmethod
    def teardown_class(cls):
        """Tear down the services required by the server."""
        super(TestTransactionInfoAPI, cls).teardown_class()
        DockerMetadata.stop_services()

    def test_transactioninfo_api(self):
        """Test the GET method."""
        main()
        start_date = datetime.datetime.utcnow().date() - datetime.timedelta(1)
        end_date = datetime.datetime.utcnow().date() + datetime.timedelta(1)

        # test by_id
        transaction_id = 67
        req = requests.get(
            '{0}/transactioninfo/by_id/{1}'.format(self.url, transaction_id))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(str(req_json['id']), str(transaction_id))

        # test search with multiple return
        search_terms = {
            'instrument': '54'
        }
        req = requests.get(
            url='{0}/transactioninfo/search/details'.format(self.url),
            params=search_terms
        )
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(len(req_json), 2)

        # test search with single return with details
        search_terms = {
            'proposal': '1234a',
            'end': end_date.strftime('%Y-%m-%d')
        }
        req = requests.get(
            url='{0}/transactioninfo/search/details'.format(self.url),
            params=search_terms
        )
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(req_json['transactions'][str(transaction_id)]['status']['trans_id'], transaction_id)
        self.assertEqual(len(req_json['transactions']), 1)

        # test date search with multiple return with details
        search_terms = {
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d'),
            'proposal': '1234a',
            'person_id': '10'
        }
        req = requests.get(
            url='{0}/transactioninfo/search/details'.format(self.url),
            params=search_terms
        )
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(req_json['transactions'][str(transaction_id)]['status']['trans_id'], transaction_id)
        self.assertEqual(len(req_json['transactions']), 1)

        # test search with single return with simple
        search_terms = {
            'proposal': '1234a',
            'start': start_date.strftime('%Y-%m-%d')
        }
        req = requests.get(
            url='{0}/transactioninfo/search/list'.format(self.url),
            params=search_terms
        )
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(len(req_json['transactions']), 1)

        # test search with transaction_id
        search_terms = {
            'transaction_id': transaction_id
        }
        req = requests.get(
            url='{0}/transactioninfo/search/list'.format(self.url),
            params=search_terms
        )
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(len(req_json['transactions']), 1)

        # test file lookup
        transaction_id = 67
        req = requests.get(
            '{0}/transactioninfo/files/{1}'.format(self.url, transaction_id))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(len(req_json), 2)

    def test_bad_transactioninfo_api(self):
        """Test the GET method with bad data."""
        # test by_id
        str_transaction_id = 'bob'
        req = requests.get(
            '{0}/transactioninfo/by_id/{1}'.format(self.url, str_transaction_id))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('Invalid Transaction ID' in req.text)

        # test with nonexistent, but valid looking id
        transaction_id = 747
        req = requests.get(
            '{0}/transactioninfo/by_id/{1}'.format(self.url, transaction_id))
        self.assertEqual(req.status_code, 404)
        self.assertTrue('No Transaction' in req.text)

        # test file lookup
        str_transaction_id = 'doug'
        req = requests.get(
            '{0}/transactioninfo/files/{1}'.format(self.url, str_transaction_id))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('Invalid Request Options' in req.text)

        # test with no search terms
        req = requests.get(
            '{0}/transactioninfo/search/details'.format(self.url))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('Invalid Request Options' in req.text)
