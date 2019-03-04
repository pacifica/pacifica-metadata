#!/usr/bin/python
# -*- coding: utf-8 -*-
"""TransactionKeyValue links Transactions and Keys and Values objects."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.base import DB
from pacifica.metadata.orm.utils import index_hash, unicode_type
from pacifica.metadata.orm.projects import Projects
from pacifica.metadata.orm.analytical_tools import AnalyticalTools
from pacifica.metadata.rest.orm import CherryPyAPI


class AToolProject(CherryPyAPI):
    """
    TransactionKeyValue attributes are foreign keys.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | project          | Link to the Projects model         |
        +-------------------+-------------------------------------+
        | analytical_tool   | Link to the AnalyticalTools model   |
        +-------------------+-------------------------------------+
    """

    project = ForeignKeyField(Projects, backref='atools')
    analytical_tool = ForeignKeyField(AnalyticalTools, backref='projects')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('analytical_tool', 'project')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(AToolProject, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(self.__data__['project']),
                                int(self.__data__['analytical_tool']))
        obj['project_id'] = unicode_type(self.__data__['project'])
        obj['analytical_tool_id'] = int(self.__data__['analytical_tool'])

        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(AToolProject, self).from_hash(obj)
        self._set_only_if('project_id', obj, 'project',
                          lambda: Projects.get(Projects.id == obj['project_id']))
        self._set_only_if('analytical_tool_id', obj, 'analytical_tool',
                          lambda: AnalyticalTools.get(
                              AnalyticalTools.id == obj['analytical_tool_id']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(AToolProject, cls).where_clause(kwargs)
        attrs = ['project', 'analytical_tool']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
