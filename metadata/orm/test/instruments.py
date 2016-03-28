#!/usr/bin/python
"""
Test the proposals ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.instruments import Instruments

SAMPLE_INSTRUMENT_HASH = {
    "instrument_id": 1234,
    "instrument_name": "My Really Long Winded Instrument Name",
    "display_name": "My Instrument Name",
    "name_short": "Instrument"
}

class TestInstruments(TestBase):
    """
    Test the Proposals ORM object
    """
    dependent_cls = []
    obj_cls = Instruments
    obj_id = Instruments.instrument_id

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
