#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Project group relationship."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.utils import index_hash, unicode_type
from pacifica.metadata.orm.projects import Projects
from pacifica.metadata.orm.groups import Groups
from pacifica.metadata.orm.base import DB
from pacifica.metadata.rest.orm import CherryPyAPI


class ProjectGroup(CherryPyAPI):
    """
    Relates projects and groups objects.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | group             | Link to the Group model             |
        +-------------------+-------------------------------------+
        | project          | Link to the Project model          |
        +-------------------+-------------------------------------+
    """

    group = ForeignKeyField(Groups, backref='projects')
    project = ForeignKeyField(Projects, backref='groups')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('group', 'project')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(ProjectGroup, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(
            self.__data__['project']), int(self.__data__['group']))
        obj['group_id'] = int(self.__data__['group'])
        obj['project_id'] = unicode_type(self.__data__['project'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(ProjectGroup, self).from_hash(obj)
        self._set_only_if(
            'project_id', obj, 'project',
            lambda: Projects.get(Projects.id == obj['project_id'])
        )
        self._set_only_if(
            'group_id', obj, 'group',
            lambda: Groups.get(Groups.id == obj['group_id'])
        )

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(ProjectGroup, cls).where_clause(kwargs)
        attrs = ['group', 'project']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
