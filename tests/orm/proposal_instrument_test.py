#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the proposal_instrument ORM object."""
from json import dumps
from pacifica.metadata.orm.proposal_instrument import ProposalInstrument
from pacifica.metadata.orm.instruments import Instruments
from pacifica.metadata.orm.proposals import Proposals
from .base_test import TestBase
from .instruments_test import SAMPLE_INSTRUMENT_HASH, TestInstruments
from .proposals_test import SAMPLE_PROPOSAL_HASH, TestProposals

SAMPLE_PROPOSAL_INSTRUMENT_HASH = {
    'proposal_id': SAMPLE_PROPOSAL_HASH['_id'],
    'instrument_id': SAMPLE_INSTRUMENT_HASH['_id']
}


class TestProposalInstrument(TestBase):
    """Test the ProposalInstrument ORM object."""

    obj_cls = ProposalInstrument
    obj_id = ProposalInstrument.proposal

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that FileKeyValue need."""
        prop2 = Proposals()
        TestProposals.base_create_dep_objs()
        prop2.from_hash(SAMPLE_PROPOSAL_HASH)
        prop2.save(force_insert=True)
        inst = Instruments()
        TestInstruments.base_create_dep_objs()
        inst.from_hash(SAMPLE_INSTRUMENT_HASH)
        inst.save(force_insert=True)

    def test_proposal_instrument_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_PROPOSAL_INSTRUMENT_HASH)

    def test_proposal_instrument_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_PROPOSAL_INSTRUMENT_HASH))

    def test_proposal_instrument_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_PROPOSAL_INSTRUMENT_HASH)
