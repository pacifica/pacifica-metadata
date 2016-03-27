#!/usr/bin/python
"""
Test the contributors ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.contributors import Contributors
from metadata.orm.test.users import SAMPLE_USER_HASH
from metadata.orm.users import Users
from metadata.orm.test.institutions import SAMPLE_INSTITUTION_HASH
from metadata.orm.institutions import Institutions

SAMPLE_CONTRIBUTOR_HASH = {
    "author_id": 192,
    "person_id": SAMPLE_USER_HASH['person_id'],
    "first_name": "John",
    "middle_initial": "F",
    "last_name": "Doe",
    "dept_code": "Ecology",
    "institution_id": SAMPLE_INSTITUTION_HASH['institution_id']
}

class TestContributors(TestBase):
    """
    Test the Institutions ORM object
    """
    dependent_cls = [Users, Institutions]
    obj_cls = Contributors
    obj_id = Contributors.author_id

    def base_create_dep_objs(self):
        """
        Create all objects that Files depend on.
        """
        inst = Institutions()
        inst.from_hash(SAMPLE_INSTITUTION_HASH)
        inst.save(force_insert=True)
        user = Users()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)

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
