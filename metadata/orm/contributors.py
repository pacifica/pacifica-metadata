#!/usr/bin/python
"""Contributors model describes an author to a journal article."""
from peewee import CharField, ForeignKeyField, Expression, OP
from metadata.orm.users import Users
from metadata.orm.institutions import Institutions
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import unicode_type


# pylint: disable=too-many-instance-attributes
class Contributors(CherryPyAPI):
    """
    Contributors object and associated fields.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | person            | Link to the User model              |
        +-------------------+-------------------------------------+
        | institution       | Link to the Institution model       |
        +-------------------+-------------------------------------+
        | first_name        | Users first name as it appears in   |
        |                   | the citation                        |
        +-------------------+-------------------------------------+
        | middle_initial    | Users middle initial as it appears  |
        |                   | in the citation                     |
        +-------------------+-------------------------------------+
        | last_name         | Users last name as it appears in    |
        |                   | the citation                        |
        +-------------------+-------------------------------------+
        | dept_code         | Department of the institution the   |
        |                   | User was a member of at the time of |
        |                   | the citation                        |
        +-------------------+-------------------------------------+
        | encoding          | Language encoding of the attributes |
        |                   | above                               |
        +-------------------+-------------------------------------+
    """

    person = ForeignKeyField(Users, related_name='contributions')
    first_name = CharField(default='')
    middle_initial = CharField(default='')
    last_name = CharField(default='')
    dept_code = CharField(default='')
    institution = ForeignKeyField(Institutions, related_name='contributors')
    encoding = CharField(default='UTF8')

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(Contributors, Contributors).elastic_mapping_builder(obj)
        obj['person_id'] = obj['institution_id'] = {'type': 'integer'}
        obj['first_name'] = obj['middle_initial'] = obj['last_name'] = \
            obj['dept_code'] = obj['encoding'] = \
            {'type': 'text', 'fields': {'keyword': {'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, recursion_depth=1):
        """Convert the object fields into a serializable hash."""
        obj = super(Contributors, self).to_hash(recursion_depth)
        obj['_id'] = int(self.id)
        obj['first_name'] = unicode_type(self.first_name)
        obj['middle_initial'] = unicode_type(self.middle_initial)
        obj['last_name'] = unicode_type(self.last_name)
        obj['dept_code'] = unicode_type(self.dept_code)
        # pylint: disable=no-member
        obj['person_id'] = int(self.person.id)
        obj['institution_id'] = int(self.institution.id)
        # pylint: enable=no-member
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object fields."""
        super(Contributors, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: int(obj['_id']))
        for attr in ['first_name', 'middle_initial', 'last_name', 'dept_code']:
            self._set_only_if(attr, obj, attr, lambda k=attr: unicode_type(obj[k]))
        self._set_only_if('person_id', obj, 'person',
                          lambda: Users.get(Users.id == int(obj['person_id'])))
        self._set_only_if('institution_id', obj, 'institution',
                          lambda: Institutions.get(Institutions.id == int(obj['institution_id'])))
        self._set_only_if('encoding', obj, 'encoding', lambda: str(obj['encoding']))

    @staticmethod
    def _where_attr_clause(where_clause, kwargs):
        for key in ['author_id', 'first_name', 'last_name', 'encoding'
                    'middle_initial', 'dept_code']:
            if key in kwargs:
                key_oper = OP.EQ
                if '{0}_operator'.format(key) in kwargs:
                    key_oper = getattr(OP, kwargs['{0}_operator'.format(key)].upper())
                where_clause &= Expression(getattr(Contributors, key), key_oper, kwargs[key])
        return where_clause

    def where_clause(self, kwargs):
        """Generate the PeeWee where clause used in searching."""
        where_clause = super(Contributors, self).where_clause(kwargs)
        if 'person_id' in kwargs:
            user = Users.get(Users.id == kwargs['person_id'])
            where_clause &= Expression(Contributors.person, OP.EQ, user)
        if 'institution_id' in kwargs:
            inst = Institutions.get(Institutions.id == kwargs['institution_id'])
            where_clause &= Expression(Contributors.institution, OP.EQ, inst)
        return self._where_attr_clause(where_clause, kwargs)
