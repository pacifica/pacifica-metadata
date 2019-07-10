#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the keys ORM object."""
from json import dumps
from datetime import datetime
from pacifica.metadata.orm.datasets import Datasets
from .base_test import TestBase

SAMPLE_DATASET_HASH = {
    '_id': 8192,
    'display_name': 'This is a really cool dataset.',
    'description': 'The really important description of the file content.',
    'suspense_date': datetime.utcnow().date().isoformat()
}


class TestDatasets(TestBase):
    """Test the Datasets ORM object."""

    obj_cls = Datasets
    obj_id = Datasets.id

    def test_dsets_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_DATASET_HASH)

    def test_dsets_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_DATASET_HASH))

    def test_dsets_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_DATASET_HASH)
