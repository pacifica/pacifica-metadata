#!/usr/bin/python
"""Test the elastic mapping class methods."""
from unittest import TestCase
from metadata.orm import ORM_OBJECTS


# pylint: disable=too-few-public-methods
class TestElastic(TestCase):
    """Test elastic mapping class methods."""

    pass
# pylint: enable=too-few-public-methods


for ORM_CLS in ORM_OBJECTS:
    def test_elastic_mapping(self, orm_cls=ORM_CLS):
        """
        Test the elasticsearch mapping method.

        check to see all types are valid both content and python types.
        """
        elastic_mapping = orm_cls.elastic_mapping()
        self.assertEqual(type(elastic_mapping), dict)
        properties = elastic_mapping['properties']
        elastic_mapping_types = ['integer', 'string', 'date', 'boolean', 'float']
        for column in properties.keys():
            self.assertEqual(properties[column]['type'] in elastic_mapping_types, True)
    setattr(TestElastic, 'test_elastic_mapping_{0}'.format(ORM_CLS.__name__.lower()), test_elastic_mapping)
