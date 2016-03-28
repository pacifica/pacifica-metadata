#!/usr/bin/python
"""
Test the file_key_values ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.proposal_participant import ProposalParticipant
from metadata.orm.test.proposals import SAMPLE_PROPOSAL_HASH
from metadata.orm.proposals import Proposals
from metadata.orm.test.users import SAMPLE_USER_HASH
from metadata.orm.users import Users

SAMPLE_PROPOSAL_PARTICIPANT_HASH = {
    "person_id": SAMPLE_USER_HASH['person_id'],
    "proposal_id": SAMPLE_PROPOSAL_HASH['proposal_id']
}

class TestProposalParticipant(TestBase):
    """
    Test the ProposalParticipant ORM object
    """
    dependent_cls = [Users, Proposals]
    obj_cls = ProposalParticipant
    obj_id = ProposalParticipant.member

    def base_create_dep_objs(self):
        """
        Create all objects that FileKeyValue need.
        """
        user = Users()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)
        prop = Proposals()
        prop.from_hash(SAMPLE_PROPOSAL_HASH)
        prop.save(force_insert=True)

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
