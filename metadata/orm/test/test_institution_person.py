#!/usr/bin/python
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.institution_person import InstitutionPerson
from metadata.orm.test.test_institutions import SAMPLE_INSTITUTION_HASH, TestInstitutions
from metadata.orm.institutions import Institutions
from metadata.orm.test.test_users import SAMPLE_USER_HASH, TestUsers
from metadata.orm.users import Users

SAMPLE_INSTITUTION_PERSON_HASH = {
    'person_id': SAMPLE_USER_HASH['_id'],
    'institution_id': SAMPLE_INSTITUTION_HASH['_id']
}


class TestInstitutionPerson(TestBase):
    """Test the InstitutionPerson ORM object."""

    obj_cls = InstitutionPerson
    obj_id = InstitutionPerson.person

    @classmethod
    def dependent_cls(cls):
        """Return dependent classes for the InstitutionPerson object."""
        ret = [InstitutionPerson]
        ret += TestUsers.dependent_cls()
        ret += TestInstitutions.dependent_cls()
        return ret

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that InstitutionPerson need."""
        inst = Institutions()
        TestInstitutions.base_create_dep_objs()
        inst.from_hash(SAMPLE_INSTITUTION_HASH)
        inst.save(force_insert=True)
        user1 = Users()
        TestUsers.base_create_dep_objs()
        user1.from_hash(SAMPLE_USER_HASH)
        user1.save(force_insert=True)

    def test_institution_person_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_INSTITUTION_PERSON_HASH)

    def test_institution_person_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_INSTITUTION_PERSON_HASH))

    def test_institution_person_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_INSTITUTION_PERSON_HASH)
