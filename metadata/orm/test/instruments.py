#!/usr/bin/python
"""
Test the proposals ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.instruments import Instruments

SAMPLE_INSTRUMENT_HASH = {
    "_id": 1234,
    "instrument_name": "My Really Long Winded Instrument Name",
    "display_name": "My Instrument Name",
    "name_short": "Instrument"
}

class TestInstruments(TestBase):
    """
    Test the Proposals ORM object
    """
    obj_cls = Instruments
    obj_id = Instruments.id

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the Instruments object
        """
        return [Instruments]

    def test_instruments_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_INSTRUMENT_HASH)

    def test_instruments_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_INSTRUMENT_HASH))

    def test_instruments_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_INSTRUMENT_HASH)

if __name__ == '__main__':
    main()
