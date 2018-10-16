#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the atool_proposal ORM object."""
from json import dumps
from pacifica.metadata.orm.atool_proposal import AToolProposal
from pacifica.metadata.orm.proposals import Proposals
from pacifica.metadata.orm.analytical_tools import AnalyticalTools
from .base_test import TestBase
from .proposals_test import SAMPLE_PROPOSAL_HASH, TestProposals
from .analytical_tools_test import SAMPLE_TOOL_HASH, TestAnalyticalTools

SAMPLE_TOOL_PROPOSAL_HASH = {
    'proposal_id': SAMPLE_PROPOSAL_HASH['_id'],
    'analytical_tool_id': SAMPLE_TOOL_HASH['_id']
}


class TestAToolProposal(TestBase):
    """Test the Keys ORM object."""

    obj_cls = AToolProposal
    obj_id = AToolProposal.proposal

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that TransactionKeyValue need."""
        prop = Proposals()
        tool = AnalyticalTools()
        TestProposals.base_create_dep_objs()
        prop.from_hash(SAMPLE_PROPOSAL_HASH)
        prop.save(force_insert=True)
        TestAnalyticalTools.base_create_dep_objs()
        tool.from_hash(SAMPLE_TOOL_HASH)
        tool.save(force_insert=True)

    def test_tool_prop_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_TOOL_PROPOSAL_HASH)

    def test_tool_prop_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_TOOL_PROPOSAL_HASH))

    def test_tool_prop_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_TOOL_PROPOSAL_HASH)
