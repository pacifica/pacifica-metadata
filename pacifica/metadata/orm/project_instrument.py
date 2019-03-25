#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Project instrument relationship."""
from peewee import ForeignKeyField, CompositeKey
from .utils import index_hash, unicode_type
from .projects import Projects
from .instruments import Instruments
from .base import DB
from ..rest.orm import CherryPyAPI


class ProjectInstrument(CherryPyAPI):
    """
    Relates projects and instrument objects.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | instrument        | Link to the Instrument model        |
        +-------------------+-------------------------------------+
        | project           | Link to the Project model          |
        +-------------------+-------------------------------------+
    """

    # NOTE: add relationship
    instrument = ForeignKeyField(Instruments, backref='projects')
    project = ForeignKeyField(Projects, backref='instruments')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('instrument', 'project')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(ProjectInstrument, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(
            self.__data__['project']), int(self.__data__['instrument']))
        obj['instrument'] = int(self.__data__['instrument'])
        obj['project'] = unicode_type(self.__data__['project'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(ProjectInstrument, self).from_hash(obj)
        self._set_only_if(
            'instrument', obj, 'instrument',
            lambda: Instruments.get(Instruments.id == obj['instrument'])
        )
        self._set_only_if(
            'project', obj, 'project',
            lambda: Projects.get(Projects.id == obj['project'])
        )

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(ProjectInstrument, cls).where_clause(kwargs)
        attrs = ['instrument', 'project']
        return cls._where_attr_clause(where_clause, kwargs, attrs)
