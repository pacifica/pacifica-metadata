#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the elastic mapping class methods."""
from unittest import TestCase
from pacifica.metadata.orm import ORM_OBJECTS


# pylint: disable=too-few-public-methods
class TestElastic(TestCase):
    """Test elastic mapping class methods."""

    def test_elastic_mapping(self):
        """
        Test the elasticsearch mapping method.

        check to see all types are valid both content and python types.
        """
        for orm_cls in ORM_OBJECTS:
            elastic_mapping = orm_cls.elastic_mapping()
            self.assertEqual(type(elastic_mapping), dict)
            properties = elastic_mapping['properties']
            elastic_mapping_types = ['integer', 'text',
                                     'keyword', 'date', 'boolean', 'float', 'long']
            for column in properties.keys():
                self.assertEqual(
                    properties[column]['type'] in elastic_mapping_types, True)
# pylint: enable=too-few-public-methods
