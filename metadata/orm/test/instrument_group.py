#!/usr/bin/python
"""
Test the user_group ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.instrument_group import InstrumentGroup
from metadata.orm.test.instruments import SAMPLE_INSTRUMENT_HASH
from metadata.orm.instruments import Instruments
from metadata.orm.test.groups import SAMPLE_GROUP_HASH
from metadata.orm.groups import Groups

SAMPLE_INSTRUMENT_GROUP_HASH = {
    "instrument_id": SAMPLE_INSTRUMENT_HASH['instrument_id'],
    "group_id": SAMPLE_GROUP_HASH['group_id']
}

class TestInstrumentGroup(TestBase):
    """
    Test the Keys ORM object
    """
    dependent_cls = [Instruments, Groups]
    obj_cls = InstrumentGroup
    obj_id = InstrumentGroup.instrument

    def base_create_dep_objs(self):
        """
        Create all objects that FileKeyValue need.
        """
        groups = Groups()
        groups.from_hash(SAMPLE_GROUP_HASH)
        groups.save(force_insert=True)
        inst = Instruments()
        inst.from_hash(SAMPLE_INSTRUMENT_HASH)
        inst.save(force_insert=True)

    def test_instrument_group_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_INSTRUMENT_GROUP_HASH)

    def test_instrument_group_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_INSTRUMENT_GROUP_HASH))

    def test_instrument_group_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_INSTRUMENT_GROUP_HASH)

if __name__ == '__main__':
    main()
