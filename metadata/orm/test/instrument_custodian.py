#!/usr/bin/python
"""
Test the file_key_values ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.instrument_custodian import InstrumentCustodian
from metadata.orm.test.instruments import SAMPLE_INSTRUMENT_HASH
from metadata.orm.instruments import Instruments
from metadata.orm.test.users import SAMPLE_USER_HASH
from metadata.orm.users import Users

SAMPLE_INSTRUMENT_CUSTODIAN_HASH = {
    "person_id": SAMPLE_USER_HASH['person_id'],
    "instrument_id": SAMPLE_INSTRUMENT_HASH['instrument_id']
}

class TestInstrumentCustodian(TestBase):
    """
    Test the InstitutionPerson ORM object
    """
    dependent_cls = [Users, Instruments]
    obj_cls = InstrumentCustodian
    obj_id = InstrumentCustodian.custodian

    def base_create_dep_objs(self):
        """
        Create all objects that FileKeyValue need.
        """
        user = Users()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)
        inst = Instruments()
        inst.from_hash(SAMPLE_INSTRUMENT_HASH)
        inst.save(force_insert=True)

    def test_instrument_custodian_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_INSTRUMENT_CUSTODIAN_HASH)

    def test_instrument_custodian_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_INSTRUMENT_CUSTODIAN_HASH))

    def test_instrument_custodian_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_INSTRUMENT_CUSTODIAN_HASH)

if __name__ == '__main__':
    main()
