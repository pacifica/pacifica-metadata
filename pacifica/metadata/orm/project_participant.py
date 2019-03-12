#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Project person relationship."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.utils import index_hash, unicode_type
from pacifica.metadata.orm.projects import Projects
from pacifica.metadata.orm.users import Users
from pacifica.metadata.orm.base import DB
from pacifica.metadata.rest.orm import CherryPyAPI


class ProjectParticipant(CherryPyAPI):
    """
    Relates projects and users objects.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | person            | Link to the Users model             |
        +-------------------+-------------------------------------+
        | project          | Link to the Projects model         |
        +-------------------+-------------------------------------+
    """

    person = ForeignKeyField(Users, backref='projects')
    project = ForeignKeyField(Projects, backref='users')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('person', 'project')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(ProjectParticipant, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(
            self.__data__['project']), int(self.__data__['person']))
        obj['person_id'] = int(self.__data__['person'])
        obj['project_id'] = unicode_type(self.__data__['project'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(ProjectParticipant, self).from_hash(obj)
        self._set_only_if('person_id', obj, 'person',
                          lambda: Users.get(Users.id == obj['person_id']))
        self._set_only_if('project_id', obj, 'project',
                          lambda: Projects.get(Projects.id == obj['project_id']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(ProjectParticipant, cls).where_clause(kwargs)
        attrs = ['person', 'project']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
