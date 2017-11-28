#!/usr/bin/python
"""Test the atool_proposal ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.atool_proposal import AToolProposal
from metadata.orm.test.test_proposals import SAMPLE_PROPOSAL_HASH, TestProposals
from metadata.orm.proposals import Proposals
from metadata.orm.test.test_analytical_tools import SAMPLE_TOOL_HASH, TestAnalyticalTools
from metadata.orm.analytical_tools import AnalyticalTools

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
