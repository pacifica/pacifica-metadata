#!/usr/bin/python
"""
Contributors model describes an author to a journal article.
"""
from peewee import CharField, ForeignKeyField, Expression, OP
from metadata.orm.users import Users
from metadata.orm.institutions import Institutions
from metadata.rest.orm import CherryPyAPI

#pylint: disable=too-many-instance-attributes
class Contributors(CherryPyAPI):
    """
    Contributors object and associated fields.
    """
    person = ForeignKeyField(Users, related_name='contributions')
    first_name = CharField(default="")
    middle_initial = CharField(default="")
    last_name = CharField(default="")
    dept_code = CharField(default="")
    institution = ForeignKeyField(Institutions, related_name='contributors')
    encoding = CharField(default="UTF8")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Contributors, Contributors).elastic_mapping_builder(obj)
        obj['person_id'] = obj['institution_id'] = {'type': 'integer'}
        obj['first_name'] = obj['middle_initial'] = obj['last_name'] = \
        obj['dept_code'] = obj['encoding'] = {'type': 'string'}

    def to_hash(self):
        """
        Convert the object fields into a serializable hash.
        """
        obj = super(Contributors, self).to_hash()
        obj['_id'] = int(self.id)
        obj['first_name'] = unicode(self.first_name)
        obj['middle_initial'] = unicode(self.middle_initial)
        obj['last_name'] = unicode(self.last_name)
        obj['person_id'] = int(self.person.id)
        obj['dept_code'] = unicode(self.dept_code)
        obj['institution_id'] = int(self.institution.id)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object fields.
        """
        super(Contributors, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = int(obj['_id'])
            # pylint: enable=invalid-name
        for attr in ['first_name', 'middle_initial', 'last_name', 'dept_code']:
            if attr in obj:
                setattr(self, attr, unicode(obj[attr]))
        if 'person_id' in obj:
            self.person = Users.get(Users.id == int(obj['person_id']))
        if 'institution_id' in obj:
            inst_bool = Institutions.id == int(obj['institution_id'])
            self.institution = Institutions.get(inst_bool)
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])

    def where_clause(self, kwargs):
        """
        Generate the PeeWee where clause used in searching.
        """
        where_clause = super(Contributors, self).where_clause(kwargs)
        if 'person_id' in kwargs:
            user = Users.get(Users.id == kwargs['person_id'])
            where_clause &= Expression(Contributors.person, OP.EQ, user)
        if 'institution_id' in kwargs:
            inst = Institutions.get(Institutions.id == kwargs['institution_id'])
            where_clause &= Expression(Contributors.institution, OP.EQ, inst)
        for key in ['author_id', 'first_name', 'last_name', 'encoding'
                    'middle_initial', 'dept_code']:
            if key in kwargs:
                where_clause &= Expression(getattr(Contributors, key), OP.EQ, kwargs[key])
        return where_clause
