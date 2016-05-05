#!/usr/bin/python
"""
Test the user_group ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.user_group import UserGroup
from metadata.orm.test.users import SAMPLE_USER_HASH
from metadata.orm.users import Users
from metadata.orm.test.groups import SAMPLE_GROUP_HASH
from metadata.orm.groups import Groups

SAMPLE_USER_GROUP_HASH = {
    "person_id": SAMPLE_USER_HASH['_id'],
    "group_id": SAMPLE_GROUP_HASH['_id']
}

class TestUserGroup(TestBase):
    """
    Test the Keys ORM object
    """
    dependent_cls = [Users, Groups]
    obj_cls = UserGroup
    obj_id = UserGroup.user

    def base_create_dep_objs(self):
        """
        Create all objects that FileKeyValue need.
        """
        groups = Groups()
        groups.from_hash(SAMPLE_GROUP_HASH)
        groups.save(force_insert=True)
        user = Users()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)

    def test_user_group_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_USER_GROUP_HASH)

    def test_user_group_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_USER_GROUP_HASH))

    def test_user_group_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_USER_GROUP_HASH)

if __name__ == '__main__':
    main()
