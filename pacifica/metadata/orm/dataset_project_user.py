#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Dataset project user relationship."""
import uuid
from peewee import ForeignKeyField, UUIDField
from ..rest.orm import CherryPyAPI
from .utils import unicode_type
from .datasets import Datasets
from .projects import Projects
from .relationships import Relationships
from .users import Users
from .base import DB


class DatasetProjectUser(CherryPyAPI):
    """
    Relates projects and users objects.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | dataset           | Link to the Datasets model          |
        +-------------------+-------------------------------------+
        | user              | Link to the Users model             |
        +-------------------+-------------------------------------+
        | project           | Link to the Projects model          |
        +-------------------+-------------------------------------+
        | relationship      | Link to the Relationships model     |
        +-------------------+-------------------------------------+
    """

    uuid = UUIDField(primary_key=True, default=uuid.uuid4, index=True)
    dataset = ForeignKeyField(Datasets, backref='userprojects')
    user = ForeignKeyField(Users, backref='datasets')
    project = ForeignKeyField(Projects, backref='datasets')
    relationship = ForeignKeyField(Relationships, backref='dataset_project_user')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        indexes = (
            (('dataset', 'user', 'project', 'relationship'), True),
        )
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(DatasetProjectUser, self).to_hash(**flags)
        obj['uuid'] = str(self.__data__['uuid'])
        obj['dataset'] = int(self.__data__['dataset'])
        obj['user'] = int(self.__data__['user'])
        obj['project'] = unicode_type(self.__data__['project'])
        obj['relationship'] = str(self.__data__['relationship'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(DatasetProjectUser, self).from_hash(obj)
        self._set_only_if('uuid', obj, 'uuid',
                          lambda: uuid.UUID(obj['uuid']))
        self._set_only_if_by_name('relationship', obj, Relationships)
        self._set_only_if(
            'dataset', obj, 'dataset',
            lambda: Datasets.get(Datasets.id == obj['dataset'])
        )
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
        where_clause = super(DatasetProjectUser, cls).where_clause(kwargs)
        attrs = ['uuid', 'dataset', 'user', 'project', 'relationship']
        return cls._where_attr_clause(where_clause, kwargs, attrs)