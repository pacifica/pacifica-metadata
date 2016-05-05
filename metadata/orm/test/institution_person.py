#!/usr/bin/python
"""
Test the file_key_values ORM object
"""
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.institution_person import InstitutionPerson
from metadata.orm.test.institutions import SAMPLE_INSTITUTION_HASH
from metadata.orm.institutions import Institutions
from metadata.orm.test.users import SAMPLE_USER_HASH
from metadata.orm.users import Users

SAMPLE_INSTITUTION_PERSON_HASH = {
    "person_id": SAMPLE_USER_HASH['_id'],
    "institution_id": SAMPLE_INSTITUTION_HASH['_id']
}

class TestInstitutionPerson(TestBase):
    """
    Test the InstitutionPerson ORM object
    """
    dependent_cls = [Users, Institutions]
    obj_cls = InstitutionPerson
    obj_id = InstitutionPerson.user

    def base_create_dep_objs(self):
        """
        Create all objects that FileKeyValue need.
        """
        user = Users()
        user.from_hash(SAMPLE_USER_HASH)
        user.save(force_insert=True)
        inst = Institutions()
        inst.from_hash(SAMPLE_INSTITUTION_HASH)
        inst.save(force_insert=True)

    def test_institution_person_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_INSTITUTION_PERSON_HASH)

    def test_institution_person_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_INSTITUTION_PERSON_HASH))

    def test_institution_person_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_INSTITUTION_PERSON_HASH)

if __name__ == '__main__':
    main()
