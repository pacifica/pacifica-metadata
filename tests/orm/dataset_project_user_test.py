#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from pacifica.metadata.orm.dataset_project_user import DatasetProjectUser
from pacifica.metadata.orm.datasets import Datasets
from pacifica.metadata.orm.projects import Projects
from pacifica.metadata.orm.users import Users
from pacifica.metadata.orm.relationships import Relationships
from .base_test import TestBase
from .datasets_test import SAMPLE_DATASET_HASH, TestDatasets
from .projects_test import SAMPLE_PROJECT_HASH, TestProjects
from .users_test import SAMPLE_USER_HASH, TestUsers
from .relationships_test import SAMPLE_RELATIONSHIP_HASH, TestRelationships

SAMPLE_DATASET_PROJECT_USER_HASH = {
    'uuid': 'dc9be2d8-a338-11e9-97e6-1a15cde0dc9b',
    'dataset': SAMPLE_DATASET_HASH['_id'],
    'user': SAMPLE_USER_HASH['_id'],
    'relationship': SAMPLE_RELATIONSHIP_HASH['uuid'],
    'project': SAMPLE_PROJECT_HASH['_id']
}


class TestDatasetProjectUser(TestBase):
    """Test the ProjectUser ORM object."""

    obj_cls = DatasetProjectUser
    obj_id = DatasetProjectUser.uuid

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that ProjectUser need."""
        dset = Datasets()
        TestDatasets.base_create_dep_objs()
        dset.from_hash(SAMPLE_DATASET_HASH)
        dset.save(force_insert=True)
        rel = Relationships()
        TestRelationships.base_create_dep_objs()
        rel.from_hash(SAMPLE_RELATIONSHIP_HASH)
        rel.save(force_insert=True)
        proj4 = Projects()
        TestProjects.base_create_dep_objs()
        proj4.from_hash(SAMPLE_PROJECT_HASH)
        proj4.save(force_insert=True)
        user = Users()
        TestUsers.base_create_dep_objs()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)

    def test_dset_project_user_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_DATASET_PROJECT_USER_HASH)

    def test_dset_project_user_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_DATASET_PROJECT_USER_HASH))

    def test_dset_project_user_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_DATASET_PROJECT_USER_HASH)
