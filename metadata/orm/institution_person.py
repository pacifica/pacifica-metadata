#!/usr/bin/python
"""
Connects a User with an Institution
"""
from peewee import ForeignKeyField, Expression, OP, CompositeKey
from metadata.orm.utils import index_hash
from metadata.orm.users import Users
from metadata.orm.institutions import Institutions
from metadata.orm.base import DB
from metadata.rest.orm import CherryPyAPI

class InstitutionPerson(CherryPyAPI):
    """
    Relates persons and institution objects.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | person            | Link to the Users model             |
        +-------------------+-------------------------------------+
        | institution       | Link to the Institutions model      |
        +-------------------+-------------------------------------+
    """
    person = ForeignKeyField(Users, related_name='institutions')
    institution = ForeignKeyField(Institutions, related_name='users')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        PeeWee meta class contains the database and the primary key.
        """
        database = DB
        primary_key = CompositeKey('person', 'institution')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(InstitutionPerson, InstitutionPerson).elastic_mapping_builder(obj)
        obj['person_id'] = obj['institution_id'] = {'type': 'integer'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(InstitutionPerson, self).to_hash()
        obj['_id'] = index_hash(int(self.person.id), int(self.institution.id))
        obj['person_id'] = int(self.person.id)
        obj['institution_id'] = int(self.institution.id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash into the object
        """
        super(InstitutionPerson, self).from_hash(obj)
        if 'person_id' in obj:
            self.person = Users.get(Users.id == obj['person_id'])
        if 'institution_id' in obj:
            self.institution = Institutions.get(
                Institutions.id == obj['institution_id']
            )

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(InstitutionPerson, self).where_clause(kwargs)
        if 'person_id' in kwargs:
            person = Users.get(Users.id == kwargs['person_id'])
            where_clause &= Expression(InstitutionPerson.person, OP.EQ, person)
        if 'institution_id' in kwargs:
            institution = Institutions.get(Institutions.id == kwargs['institution_id'])
            where_clause &= Expression(InstitutionPerson.institution, OP.EQ, institution)
        return where_clause
