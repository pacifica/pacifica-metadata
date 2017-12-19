#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.instrument_custodian import InstrumentCustodian
from metadata.orm.test.test_instruments import SAMPLE_INSTRUMENT_HASH, TestInstruments
from metadata.orm.instruments import Instruments
from metadata.orm.test.test_users import SAMPLE_USER_HASH, TestUsers
from metadata.orm.users import Users

SAMPLE_INSTRUMENT_CUSTODIAN_HASH = {
    'custodian_id': SAMPLE_USER_HASH['_id'],
    'instrument_id': SAMPLE_INSTRUMENT_HASH['_id']
}


class TestInstrumentCustodian(TestBase):
    """Test the InstitutionPerson ORM object."""

    obj_cls = InstrumentCustodian
    obj_id = InstrumentCustodian.custodian

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that InstrumentCustodian need."""
        inst = Instruments()
        TestInstruments.base_create_dep_objs()
        inst.from_hash(SAMPLE_INSTRUMENT_HASH)
        inst.save(force_insert=True)
        custodian = Users()
        TestUsers.base_create_dep_objs()
        custodian.from_hash(SAMPLE_USER_HASH)
        custodian.save(force_insert=True)

    def test_instrument_custodian_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_INSTRUMENT_CUSTODIAN_HASH)

    def test_instrument_custodian_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_INSTRUMENT_CUSTODIAN_HASH))

    def test_instrument_custodian_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_INSTRUMENT_CUSTODIAN_HASH)
