#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the dataset_file ORM object."""
from json import dumps
from pacifica.metadata.orm.dataset_file import DatasetFile
from pacifica.metadata.orm.datasets import Datasets
from pacifica.metadata.orm.files import Files
from .base_test import TestBase
from .datasets_test import SAMPLE_DATASET_HASH, TestDatasets
from .files_test import SAMPLE_FILE_HASH, TestFiles

SAMPLE_DATASET_FILE_HASH = {
    'dataset': SAMPLE_DATASET_HASH['_id'],
    'file': SAMPLE_FILE_HASH['_id']
}


class TestDatasetFile(TestBase):
    """Test the DatasetFile ORM object."""

    obj_cls = DatasetFile
    obj_id = DatasetFile.dataset

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that TransactionKeyValue need."""
        dset = Datasets()
        files = Files()
        TestDatasets.base_create_dep_objs()
        dset.from_hash(SAMPLE_DATASET_HASH)
        dset.save(force_insert=True)
        TestFiles.base_create_dep_objs()
        files.from_hash(SAMPLE_FILE_HASH)
        files.save(force_insert=True)

    def test_dset_file_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_DATASET_FILE_HASH)

    def test_dset_file_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_DATASET_FILE_HASH))

    def test_dset_file_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_DATASET_FILE_HASH)
