#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the keys ORM object."""
from json import dumps
from datetime import datetime
from pacifica.metadata.orm.transactions import Transactions
from pacifica.metadata.orm.users import Users
from pacifica.metadata.orm.proposals import Proposals
from pacifica.metadata.orm.instruments import Instruments
from .base_test import TestBase
from .users_test import SAMPLE_USER_HASH as SAMPLE_SUBMITTER_HASH, TestUsers
from .proposals_test import SAMPLE_PROPOSAL_HASH, TestProposals
from .instruments_test import SAMPLE_INSTRUMENT_HASH, TestInstruments

SAMPLE_TRANSACTION_HASH = {
    '_id': 127,
    'submitter': SAMPLE_SUBMITTER_HASH['_id'],
    'proposal': SAMPLE_PROPOSAL_HASH['_id'],
    'instrument': SAMPLE_INSTRUMENT_HASH['_id'],
    'suspense_date': datetime.utcnow().date().isoformat()
}


class TestTransactions(TestBase):
    """Test the Transactions ORM object."""

    obj_cls = Transactions
    obj_id = Transactions.id

    @classmethod
    def base_create_dep_objs(cls):
        """Build the object and make dependent user object."""
        submitter, _created = Users().get_or_create(
            id=SAMPLE_SUBMITTER_HASH['_id'])
        TestUsers.base_create_dep_objs()
        submitter.from_hash(SAMPLE_SUBMITTER_HASH)
        submitter.save()
        prop = Proposals()
        TestProposals.base_create_dep_objs()
        prop.from_hash(SAMPLE_PROPOSAL_HASH)
        prop.save(force_insert=True)
        inst = Instruments()
        TestInstruments.base_create_dep_objs()
        inst.from_hash(SAMPLE_INSTRUMENT_HASH)
        inst.save(force_insert=True)

    def test_transactions_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_TRANSACTION_HASH)

    def test_transactions_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_TRANSACTION_HASH))

    def test_transactions_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_TRANSACTION_HASH)
