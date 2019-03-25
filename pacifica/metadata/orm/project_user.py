#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Project user relationship."""
from peewee import ForeignKeyField, CompositeKey
from ..rest.orm import CherryPyAPI
from .utils import index_hash, unicode_type
from .projects import Projects
from .users import Users
from .base import DB


class ProjectUser(CherryPyAPI):
    """
    Relates projects and users objects.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | user              | Link to the Users model             |
        +-------------------+-------------------------------------+
        | project           | Link to the Projects model          |
        +-------------------+-------------------------------------+
    """

    # NOTE: add relationship
    user = ForeignKeyField(Users, backref='projects')
    project = ForeignKeyField(Projects, backref='users')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('user', 'project')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(ProjectUser, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(
            self.__data__['project']), int(self.__data__['user']))
        obj['user'] = int(self.__data__['user'])
        obj['project'] = unicode_type(self.__data__['project'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(ProjectUser, self).from_hash(obj)
        self._set_only_if(
            'user', obj, 'user',
            lambda: Users.get(Users.id == obj['user'])
        )
        self._set_only_if(
            'project', obj, 'project',
            lambda: Projects.get(Projects.id == obj['project'])
        )

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(ProjectUser, cls).where_clause(kwargs)
        attrs = ['user', 'project']
        return cls._where_attr_clause(where_clause, kwargs, attrs)
