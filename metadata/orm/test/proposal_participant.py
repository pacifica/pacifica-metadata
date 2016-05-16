#!/usr/bin/python
"""
Test the file_key_values ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.proposal_participant import ProposalParticipant
from metadata.orm.test.proposals import SAMPLE_PROPOSAL_HASH, TestProposals
from metadata.orm.proposals import Proposals
from metadata.orm.test.users import SAMPLE_USER_HASH, TestUsers
from metadata.orm.users import Users

SAMPLE_PROPOSAL_PARTICIPANT_HASH = {
    "person_id": SAMPLE_USER_HASH['_id'],
    "proposal_id": SAMPLE_PROPOSAL_HASH['_id']
}

class TestProposalParticipant(TestBase):
    """
    Test the ProposalParticipant ORM object
    """
    obj_cls = ProposalParticipant
    obj_id = ProposalParticipant.member

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the ProposalParticipant object
        """
        ret = [ProposalParticipant]
        ret += TestProposals.dependent_cls()
        ret += TestUsers.dependent_cls()
        return ret

    @classmethod
    def base_create_dep_objs(cls):
        """
        Create all objects that ProposalParticipant need.
        """
        prop3 = Proposals()
        TestProposals.base_create_dep_objs()
        prop3.from_hash(SAMPLE_PROPOSAL_HASH)
        prop3.save(force_insert=True)
        user = Users()
        TestUsers.base_create_dep_objs()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)

    def test_proposal_participant_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_PROPOSAL_PARTICIPANT_HASH)

    def test_proposal_participant_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_PROPOSAL_PARTICIPANT_HASH))

    def test_proposal_participant_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_PROPOSAL_PARTICIPANT_HASH)

if __name__ == '__main__':
    main()
