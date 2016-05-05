#!/usr/bin/python
"""
Test the proposal_instrument ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.proposal_instrument import ProposalInstrument
from metadata.orm.test.instruments import SAMPLE_INSTRUMENT_HASH
from metadata.orm.instruments import Instruments
from metadata.orm.test.proposals import SAMPLE_PROPOSAL_HASH
from metadata.orm.proposals import Proposals

SAMPLE_PROPOSAL_INSTRUMENT_HASH = {
    "proposal_id": SAMPLE_PROPOSAL_HASH['_id'],
    "instrument_id": SAMPLE_INSTRUMENT_HASH['_id']
}

class TestProposalInstrument(TestBase):
    """
    Test the ProposalInstrument ORM object
    """
    dependent_cls = [Proposals, Instruments]
    obj_cls = ProposalInstrument
    obj_id = ProposalInstrument.proposal

    def base_create_dep_objs(self):
        """
        Create all objects that FileKeyValue need.
        """
        inst = Instruments()
        inst.from_hash(SAMPLE_INSTRUMENT_HASH)
        inst.save(force_insert=True)
        prop = Proposals()
        prop.from_hash(SAMPLE_PROPOSAL_HASH)
        prop.save(force_insert=True)

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

if __name__ == '__main__':
    main()
