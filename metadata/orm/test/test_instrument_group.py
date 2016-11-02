#!/usr/bin/python
"""Test the user_group ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.instrument_group import InstrumentGroup
from metadata.orm.test.test_instruments import SAMPLE_INSTRUMENT_HASH, TestInstruments
from metadata.orm.instruments import Instruments
from metadata.orm.test.test_groups import SAMPLE_GROUP_HASH, TestGroups
from metadata.orm.groups import Groups

SAMPLE_INSTRUMENT_GROUP_HASH = {
    'instrument_id': SAMPLE_INSTRUMENT_HASH['_id'],
    'group_id': SAMPLE_GROUP_HASH['_id']
}


class TestInstrumentGroup(TestBase):
    """Test the Keys ORM object."""

    obj_cls = InstrumentGroup
    obj_id = InstrumentGroup.instrument

    @classmethod
    def dependent_cls(cls):
        """Return dependent classes for the InstrumentGroup object."""
        ret = [InstrumentGroup]
        ret += TestInstruments.dependent_cls()
        ret += TestGroups.dependent_cls()
        return ret

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that InstrumentGroup need."""
        groups = Groups()
        TestGroups.base_create_dep_objs()
        groups.from_hash(SAMPLE_GROUP_HASH)
        groups.save(force_insert=True)
        inst = Instruments()
        TestInstruments.base_create_dep_objs()
        inst.from_hash(SAMPLE_INSTRUMENT_HASH)
        inst.save(force_insert=True)

    def test_instrument_group_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_INSTRUMENT_GROUP_HASH)

    def test_instrument_group_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_INSTRUMENT_GROUP_HASH))

    def test_instrument_group_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_INSTRUMENT_GROUP_HASH)
