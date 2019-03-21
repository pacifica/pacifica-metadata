#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Connects a User with an Institution."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.utils import index_hash
from pacifica.metadata.orm.users import Users
from pacifica.metadata.orm.institutions import Institutions
from pacifica.metadata.orm.base import DB
from pacifica.metadata.rest.orm import CherryPyAPI


class InstitutionUser(CherryPyAPI):
    """
    Relates persons and institution objects.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | user              | Link to the Users model             |
        +-------------------+-------------------------------------+
        | institution       | Link to the Institutions model      |
        +-------------------+-------------------------------------+
    """

    # NOTE: add relationship
    user = ForeignKeyField(Users, backref='institutions')
    institution = ForeignKeyField(Institutions, backref='users')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('user', 'institution')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(InstitutionUser, self).to_hash(**flags)
        obj['_id'] = index_hash(int(self.__data__['user']),
                                int(self.__data__['institution']))
        obj['user'] = int(self.__data__['user'])
        obj['institution'] = int(self.__data__['institution'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(InstitutionUser, self).from_hash(obj)
        self._set_only_if(
            'user', obj, 'user',
            lambda: Users.get(Users.id == obj['user'])
        )
        self._set_only_if(
            'institution', obj, 'institution',
            lambda: Institutions.get(Institutions.id == obj['institution'])
        )

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(InstitutionUser, cls).where_clause(kwargs)
        attrs = ['user', 'institution']
        return cls._where_attr_clause(where_clause, kwargs, attrs)
