#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the ORM interface DOIUpload."""
from json import loads
from os.path import realpath
import requests
from . import CPCommonTest


class TestDOIUploadAPI(CPCommonTest):
    """Test the DOIUploadAPI class."""

    __test__ = True

    def test_doiupload_api(self):
        """Test the POST method."""
        entry_path = realpath('test_files')
        entry_data = loads(open(
            '{0}/{1}.json'.format(
                entry_path,
                'doiupload_api'
            )
        ).read())

        header_list = {'Content-Type': 'application/json'}
        req = requests.post(
            url='{0}/doiupload/new_entry'.format(self.url),
            json=entry_data,
            headers=header_list
        )
        self.assertEqual(req.status_code, 200)

        # test for unreleased transaction_id
        entry_data['doi'] = entry_data['doi'].replace('.67', '.68')
        entry_data['meta']['doi_infix'] = entry_data['meta']['doi_infix'].replace(
            '.67', '.68')
        entry_data['meta']['site_url'] = entry_data['meta']['site_url'].replace(
            '/67', '/68')

        req = requests.post(
            url='{0}/doiupload/new_entry'.format(self.url),
            json=entry_data,
            headers=header_list
        )
        self.assertEqual(req.status_code, 400)
        self.assertTrue('has not been released' in req.text)

    def test_osti_update(self):
        """Test the POST method for information updates."""
        path = realpath('test_files')
        update_data = open(
            '{0}/{1}.xml'.format(
                path,
                'osti_update'
            )
        ).read()

        header_list = {'Content-Type': 'application/xml'}
        req = requests.post(
            url='{0}/doiupload/update'.format(self.url),
            data=update_data,
            headers=header_list
        )

        self.assertEqual(req.status_code, 200)

        update_data = open(
            '{0}/{1}.xml'.format(
                path,
                'osti_update_missing_trans'
            )
        ).read()

        req = requests.post(
            url='{0}/doiupload/update'.format(self.url),
            data=update_data,
            headers=header_list
        )

        self.assertEqual(req.status_code, 404)

        update_data = open(
            '{0}/{1}.xml'.format(
                path,
                'osti_update_bad'
            )
        ).read()

        req = requests.post(
            url='{0}/doiupload/update'.format(self.url),
            data=update_data,
            headers=header_list
        )
        self.assertEqual(req.status_code, 400)

    #     req = requests.get(
    #         '{0}/objectinfo?object_class_name=list'.format(self.url))
    #     self.assertEqual(req.status_code, 200)
    #     req_json = loads(req.text)
    #     self.assertTrue('available_objects' in req_json)
    #     req_default = requests.get(
    #         '{0}/objectinfo?object_class_name=Keys'.format(self.url))
    #     req_explicit = requests.get(
    #         '{0}/objectinfo?object_class_name=Keys&operation=overview'.format(self.url))
    #     self.assertEqual(req_default.status_code, 200)
    #     self.assertEqual(req_explicit.status_code, 200)
    #     self.assertEqual(req_default.text, req_explicit.text)
    #     req_json = loads(req_default.text)
    #     self.assertTrue('record_count' in req_json)
    #     self.assertEqual(req_json['record_count'], 2)
    #     req = requests.get(
    #         '{0}/objectinfo?object_class_name=Keys&operation=hashlist'.format(self.url))
    #     self.assertEqual(req.status_code, 200)
    #     req_json = loads(req.text)
    #     self.assertTrue('hash_list' in req_json)
    #     self.assertTrue('hash_lookup' in req_json)
    #
    # def test_bad_objectinfo_api(self):
    #     """Test the GET method with bad data."""
    #     req = requests.get(
    #         '{0}/objectinfo?object_class_name=DoesNotExist'.format(self.url))
    #     self.assertEqual(req.status_code, 404)
    #     self.assertTrue(
    #         "'DoesNotExist' is not a valid class object name" in req.text)
    #     req = requests.get('{0}/objectinfo'.format(self.url))
    #     self.assertEqual(req.status_code, 404)
    #     self.assertTrue('No object class name found' in req.text)
