#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from pacifica.metadata.orm.project_user import ProjectUser
from pacifica.metadata.orm.projects import Projects
from pacifica.metadata.orm.users import Users
from .base_test import TestBase
from .projects_test import SAMPLE_PROJECT_HASH, TestProjects
from .users_test import SAMPLE_USER_HASH, TestUsers

SAMPLE_PROJECT_USER_HASH = {
    'user': SAMPLE_USER_HASH['_id'],
    'project': SAMPLE_PROJECT_HASH['_id']
}


class TestProjectUser(TestBase):
    """Test the ProjectUser ORM object."""

    obj_cls = ProjectUser
    obj_id = ProjectUser.user

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that ProjectUser need."""
        proj3 = Projects()
        TestProjects.base_create_dep_objs()
        proj3.from_hash(SAMPLE_PROJECT_HASH)
        proj3.save(force_insert=True)
        user = Users()
        TestUsers.base_create_dep_objs()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)

    def test_project_user_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_PROJECT_USER_HASH)

    def test_project_user_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_PROJECT_USER_HASH))

    def test_project_user_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_PROJECT_USER_HASH)
