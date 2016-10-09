#!/usr/bin/python
"""
Test the proposal_instrument ORM object
"""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.proposal_instrument import ProposalInstrument
from metadata.orm.test.instruments import SAMPLE_INSTRUMENT_HASH, TestInstruments
from metadata.orm.instruments import Instruments
from metadata.orm.test.proposals import SAMPLE_PROPOSAL_HASH, TestProposals
from metadata.orm.proposals import Proposals

SAMPLE_PROPOSAL_INSTRUMENT_HASH = {
    "proposal_id": SAMPLE_PROPOSAL_HASH['_id'],
    "instrument_id": SAMPLE_INSTRUMENT_HASH['_id']
}

class TestProposalInstrument(TestBase):
    """
    Test the ProposalInstrument ORM object
    """
    obj_cls = ProposalInstrument
    obj_id = ProposalInstrument.proposal

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the ProposalInstrument object
        """
        ret = [ProposalInstrument]
        ret += TestProposals.dependent_cls()
        ret += TestInstruments.dependent_cls()
        return ret

    @classmethod
    def base_create_dep_objs(cls):
        """
        Create all objects that FileKeyValue need.
        """
        prop2 = Proposals()
        TestProposals.base_create_dep_objs()
        prop2.from_hash(SAMPLE_PROPOSAL_HASH)
        prop2.save(force_insert=True)
        inst = Instruments()
        TestInstruments.base_create_dep_objs()
        inst.from_hash(SAMPLE_INSTRUMENT_HASH)
        inst.save(force_insert=True)

    def test_proposal_instrument_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_PROPOSAL_INSTRUMENT_HASH)

    def test_proposal_instrument_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_PROPOSAL_INSTRUMENT_HASH))

    def test_proposal_instrument_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_PROPOSAL_INSTRUMENT_HASH)
