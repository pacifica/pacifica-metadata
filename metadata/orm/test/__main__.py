#!/usr/bin/python
"""
Test all the objects
"""
from unittest import main
#pylint: disable=unused-import
from metadata.orm.test.users import TestUsers
from metadata.orm.test.transactions import TestTransactions
from metadata.orm.test.files import TestFiles
from metadata.orm.test.keys import TestKeys
from metadata.orm.test.values import TestValues
from metadata.orm.test.dbdates import TestDBDates
#pylint: enable=unused-import

if __name__ == '__main__':
    main()
