#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Connects a User with an Institution."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.utils import index_hash
from pacifica.metadata.orm.users import Users
from pacifica.metadata.orm.institutions import Institutions
from pacifica.metadata.orm.base import DB
from pacifica.metadata.rest.orm import CherryPyAPI


class InstitutionPerson(CherryPyAPI):
    """
    Relates persons and institution objects.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | person            | Link to the Users model             |
        +-------------------+-------------------------------------+
        | institution       | Link to the Institutions model      |
        +-------------------+-------------------------------------+
    """

    person = ForeignKeyField(Users, backref='institutions')
    institution = ForeignKeyField(Institutions, backref='users')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('person', 'institution')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(InstitutionPerson, self).to_hash(**flags)
        obj['_id'] = index_hash(int(self.__data__['person']),
                                int(self.__data__['institution']))
        obj['person_id'] = int(self.__data__['person'])
        obj['institution_id'] = int(self.__data__['institution'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(InstitutionPerson, self).from_hash(obj)
        self._set_only_if('person_id', obj, 'person',
                          lambda: Users.get(Users.id == obj['person_id']))
        self._set_only_if('institution_id', obj, 'institution',
                          lambda: Institutions.get(Institutions.id == obj['institution_id']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(InstitutionPerson, cls).where_clause(kwargs)
        attrs = ['person', 'institution']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
