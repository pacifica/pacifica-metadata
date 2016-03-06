#!/usr/bin/python
"""
Test the keys ORM object
"""
from base import TestBase
from metadata.orm.keys import Keys
from unittest import main

class TestKeys(TestBase):
    obj_cls = Keys
    obj_id = Keys.key_id
    pass

if __name__ == '__main__':
    main()
