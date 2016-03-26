#!/usr/bin/python
"""
Test the file_key_values ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.file_key_value import FileKeyValue
from metadata.orm.test.transactions import SAMPLE_TRANSACTION_HASH
from metadata.orm.transactions import Transactions
from metadata.orm.test.users import SAMPLE_USER_HASH
from metadata.orm.users import Users
from metadata.orm.test.files import SAMPLE_FILE_HASH
from metadata.orm.files import Files
from metadata.orm.test.keys import SAMPLE_KEY_HASH
from metadata.orm.keys import Keys
from metadata.orm.test.values import SAMPLE_VALUE_HASH
from metadata.orm.values import Values

SAMPLE_FILE_KEY_VALUE_HASH = {
    "file_id": SAMPLE_FILE_HASH['file_id'],
    "key_id": SAMPLE_KEY_HASH['key_id'],
    "value_id": SAMPLE_VALUE_HASH['value_id']
}

class TestFileKeyValue(TestBase):
    """
    Test the Keys ORM object
    """
    dependent_cls = [Users, Transactions, Files, Keys, Values]
    obj_cls = FileKeyValue
    obj_id = FileKeyValue.file

    def base_create_dep_objs(self):
        """
        Create all objects that FileKeyValue need.
        """
        user = Users()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)
        keys = Keys()
        keys.from_hash(SAMPLE_KEY_HASH)
        keys.save(force_insert=True)
        trans = Transactions()
        trans.from_hash(SAMPLE_TRANSACTION_HASH)
        trans.save(force_insert=True)
        values = Values()
        values.from_hash(SAMPLE_VALUE_HASH)
        values.save(force_insert=True)
        files = Files()
        files.from_hash(SAMPLE_FILE_HASH)
        files.save(force_insert=True)

    def test_file_key_value_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_FILE_KEY_VALUE_HASH)

    def test_file_key_value_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_FILE_KEY_VALUE_HASH))

    def test_file_key_value_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_FILE_KEY_VALUE_HASH)

if __name__ == '__main__':
    main()
