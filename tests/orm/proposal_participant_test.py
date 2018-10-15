#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from pacifica.metadata.orm.proposal_participant import ProposalParticipant
from pacifica.metadata.orm.proposals import Proposals
from pacifica.metadata.orm.users import Users
from .base_test import TestBase
from .proposals_test import SAMPLE_PROPOSAL_HASH, TestProposals
from .users_test import SAMPLE_USER_HASH, TestUsers

SAMPLE_PROPOSAL_PARTICIPANT_HASH = {
    'person_id': SAMPLE_USER_HASH['_id'],
    'proposal_id': SAMPLE_PROPOSAL_HASH['_id']
}


class TestProposalParticipant(TestBase):
    """Test the ProposalParticipant ORM object."""

    obj_cls = ProposalParticipant
    obj_id = ProposalParticipant.person

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that ProposalParticipant need."""
        prop3 = Proposals()
        TestProposals.base_create_dep_objs()
        prop3.from_hash(SAMPLE_PROPOSAL_HASH)
        prop3.save(force_insert=True)
        user = Users()
        TestUsers.base_create_dep_objs()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)

    def test_proposal_participant_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_PROPOSAL_PARTICIPANT_HASH)

    def test_proposal_participant_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_PROPOSAL_PARTICIPANT_HASH))

    def test_proposal_participant_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_PROPOSAL_PARTICIPANT_HASH)
