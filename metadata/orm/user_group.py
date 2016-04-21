#!/usr/bin/python
"""
UserGroup links Groups and Users and objects.
"""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.base import DB
from metadata.rest.orm import CherryPyAPI
from metadata.orm.groups import Groups
from metadata.orm.users import Users

class UserGroup(CherryPyAPI):
    """
    UserGroup attributes are foreign keys.
    """
    user = ForeignKeyField(Users, related_name='groups')
    group = ForeignKeyField(Groups, related_name='user_members')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        PeeWee meta class contains the database and the primary key.
        """
        database = DB
        primary_key = CompositeKey('user', 'group')
    # pylint: enable=too-few-public-methods

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(UserGroup, self).to_hash()
        obj['person_id'] = int(self.user.person_id)
        obj['group_id'] = int(self.group.group_id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash into the object
        """
        super(UserGroup, self).from_hash(obj)
        if 'person_id' in obj:
            self.user = Users.get(Users.person_id == obj['person_id'])
        if 'group_id' in obj:
            self.group = Groups.get(Groups.group_id == obj['group_id'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(UserGroup, self).where_clause(kwargs)
        if 'person_id' in kwargs:
            user = Users.get(Users.person_id == kwargs['person_id'])
            where_clause &= Expression(UserGroup.user, OP.EQ, user)
        if 'group_id' in kwargs:
            group = Groups.get(Groups.group_id == kwargs['group_id'])
            where_clause &= Expression(UserGroup.group, OP.EQ, group)
        return where_clause

