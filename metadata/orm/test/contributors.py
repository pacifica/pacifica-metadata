#!/usr/bin/python
"""
Test the contributors ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.contributors import Contributors
from metadata.orm.test.users import SAMPLE_USER_HASH, TestUsers
from metadata.orm.users import Users
from metadata.orm.test.institutions import SAMPLE_INSTITUTION_HASH, TestInstitutions
from metadata.orm.institutions import Institutions

SAMPLE_CONTRIBUTOR_HASH = {
    "_id": 192,
    "person_id": SAMPLE_USER_HASH['_id'],
    "first_name": "John",
    "middle_initial": "F",
    "last_name": "Doe",
    "dept_code": "Ecology",
    "institution_id": SAMPLE_INSTITUTION_HASH['_id']
}

class TestContributors(TestBase):
    """
    Test the Institutions ORM object
    """
    obj_cls = Contributors
    obj_id = Contributors.id

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the Contributors object
        """
        ret = [Contributors]
        ret += TestInstitutions.dependent_cls()
        ret += TestUsers.dependent_cls()
        return ret

    @classmethod
    def base_create_dep_objs(cls):
        """
        Create all objects that Files depend on.
        """
        user = Users()
        TestUsers.base_create_dep_objs()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)
        inst = Institutions()
        TestInstitutions.base_create_dep_objs()
        inst.from_hash(SAMPLE_INSTITUTION_HASH)
        inst.save(force_insert=True)

    def test_contributors_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_CONTRIBUTOR_HASH)

    def test_contributors_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_CONTRIBUTOR_HASH))

    def test_contributors_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_CONTRIBUTOR_HASH)

if __name__ == '__main__':
    main()
