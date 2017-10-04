#!/usr/bin/python
"""Test the keys ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.transactions import Transactions
from metadata.orm.test.test_users import SAMPLE_USER_HASH as SAMPLE_SUBMITTER_HASH
from metadata.orm.test.test_users import TestUsers
from metadata.orm.users import Users
from metadata.orm.test.test_proposals import SAMPLE_PROPOSAL_HASH, TestProposals
from metadata.orm.proposals import Proposals
from metadata.orm.test.test_instruments import SAMPLE_INSTRUMENT_HASH, TestInstruments
from metadata.orm.instruments import Instruments

SAMPLE_TRANSACTION_HASH = {
    '_id': 127,
    'submitter': SAMPLE_SUBMITTER_HASH['_id'],
    'proposal': SAMPLE_PROPOSAL_HASH['_id'],
    'instrument': SAMPLE_INSTRUMENT_HASH['_id']
}


class TestTransactions(TestBase):
    """Test the Transactions ORM object."""

    obj_cls = Transactions
    obj_id = Transactions.id

    @classmethod
    def base_create_dep_objs(cls):
        """Build the object and make dependent user object."""
        submitter = Users()
        TestUsers.base_create_dep_objs()
        submitter.from_hash(SAMPLE_SUBMITTER_HASH)
        submitter.save(force_insert=True)
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
