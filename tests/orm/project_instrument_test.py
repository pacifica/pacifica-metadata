#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the project_instrument ORM object."""
from json import dumps
from pacifica.metadata.orm.project_instrument import ProjectInstrument
from pacifica.metadata.orm.instruments import Instruments
from pacifica.metadata.orm.projects import Projects
from .base_test import TestBase
from .instruments_test import SAMPLE_INSTRUMENT_HASH, TestInstruments
from .projects_test import SAMPLE_PROJECT_HASH, TestProjects

SAMPLE_PROJECT_INSTRUMENT_HASH = {
    'project_id': SAMPLE_PROJECT_HASH['_id'],
    'instrument_id': SAMPLE_INSTRUMENT_HASH['_id']
}


class TestProjectInstrument(TestBase):
    """Test the ProjectInstrument ORM object."""

    obj_cls = ProjectInstrument
    obj_id = ProjectInstrument.project

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that FileKeyValue need."""
        proj2 = Projects()
        TestProjects.base_create_dep_objs()
        proj2.from_hash(SAMPLE_PROJECT_HASH)
        proj2.save(force_insert=True)
        inst = Instruments()
        TestInstruments.base_create_dep_objs()
        inst.from_hash(SAMPLE_INSTRUMENT_HASH)
        inst.save(force_insert=True)

    def test_project_instrument_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_PROJECT_INSTRUMENT_HASH)

    def test_project_instrument_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_PROJECT_INSTRUMENT_HASH))

    def test_project_instrument_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_PROJECT_INSTRUMENT_HASH)
