#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the proposal_group ORM object."""
from json import dumps
from pacifica.metadata.orm.proposal_group import ProposalGroup
from pacifica.metadata.orm.groups import Groups
from pacifica.metadata.orm.proposals import Proposals
from .base_test import TestBase
from .groups_test import SAMPLE_GROUP_HASH, TestGroups
from .proposals_test import SAMPLE_PROPOSAL_HASH, TestProposals

SAMPLE_PROPOSAL_GROUP_HASH = {
    'proposal_id': SAMPLE_PROPOSAL_HASH['_id'],
    'group_id': SAMPLE_GROUP_HASH['_id']
}


class TestProposalGroup(TestBase):
    """Test the ProposalGroup ORM object."""

    obj_cls = ProposalGroup
    obj_id = ProposalGroup.proposal

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that ProposalGroup need."""
        grp = Groups()
        TestGroups.base_create_dep_objs()
        grp.from_hash(SAMPLE_GROUP_HASH)
        grp.save(force_insert=True)
        prop2 = Proposals()
        TestProposals.base_create_dep_objs()
        prop2.from_hash(SAMPLE_PROPOSAL_HASH)
        prop2.save(force_insert=True)

    def test_proposal_group_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_PROPOSAL_GROUP_HASH)

    def test_proposal_group_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_PROPOSAL_GROUP_HASH))

    def test_proposal_group_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_PROPOSAL_GROUP_HASH)
