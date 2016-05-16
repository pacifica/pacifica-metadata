#!/usr/bin/python
"""
Test the user_group ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.user_group import UserGroup
from metadata.orm.test.users import SAMPLE_USER_HASH, TestUsers
from metadata.orm.users import Users
from metadata.orm.test.groups import SAMPLE_GROUP_HASH, TestGroups
from metadata.orm.groups import Groups

SAMPLE_USER_GROUP_HASH = {
    "person_id": SAMPLE_USER_HASH['_id'],
    "group_id": SAMPLE_GROUP_HASH['_id']
}

class TestUserGroup(TestBase):
    """
    Test the Keys ORM object
    """
    obj_cls = UserGroup
    obj_id = UserGroup.user

    @classmethod
    def dependent_cls(cls):
        ret = [UserGroup]
        ret += TestUsers.dependent_cls()
        ret += TestGroups.dependent_cls()
        return ret

    @classmethod
    def base_create_dep_objs(cls):
        """
        Create all objects that FileKeyValue need.
        """
        groups = Groups()
        TestGroups.base_create_dep_objs()
        groups.from_hash(SAMPLE_GROUP_HASH)
        groups.save(force_insert=True)
        user = Users()
        TestUsers.base_create_dep_objs()
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
