#!/usr/bin/python
"""UserGroup links Groups and Users and objects."""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.utils import index_hash
from metadata.orm.base import DB
from metadata.rest.orm import CherryPyAPI
from metadata.orm.groups import Groups
from metadata.orm.users import Users


class UserGroup(CherryPyAPI):
    """
    UserGroup attributes are foreign keys.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | person            | Link to the Users model             |
        +-------------------+-------------------------------------+
        | group             | Link to the Groups model            |
        +-------------------+-------------------------------------+
    """

    person = ForeignKeyField(Users, related_name='groups')
    group = ForeignKeyField(Groups, related_name='members')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('person', 'group')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(UserGroup, UserGroup).elastic_mapping_builder(obj)
        obj['group_id'] = obj['person_id'] = {'type': 'integer'}

    def to_hash(self, flags):
        """Convert the object to a hash."""
        obj = super(UserGroup, self).to_hash(flags)
        obj['_id'] = index_hash(int(self.person.id), int(self.group.id))
        obj['person_id'] = int(self.person.id)
        obj['group_id'] = int(self.group.id)
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(UserGroup, self).from_hash(obj)
        if 'person_id' in obj:
            self.person = Users.get(Users.id == obj['person_id'])
        if 'group_id' in obj:
            self.group = Groups.get(Groups.id == obj['group_id'])

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(UserGroup, self).where_clause(kwargs)
        if 'person_id' in kwargs:
            user = Users.get(Users.id == kwargs['person_id'])
            where_clause &= Expression(UserGroup.person, OP.EQ, user)
        if 'group_id' in kwargs:
            group = Groups.get(Groups.id == kwargs['group_id'])
            where_clause &= Expression(UserGroup.group, OP.EQ, group)
        return where_clause
