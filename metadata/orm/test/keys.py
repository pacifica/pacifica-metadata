#!/usr/bin/python
"""
Test the keys ORM object
"""
from unittest import main
from metadata.orm.test.base import TestBase
from metadata.orm.keys import Keys

class TestKeys(TestBase):
    """
    Test the Keys ORM object
    """
    obj_cls = Keys
    obj_id = Keys.key_id

if __name__ == '__main__':
    main()
