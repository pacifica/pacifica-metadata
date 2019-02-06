#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Proposal person relationship."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.utils import index_hash, unicode_type
from pacifica.metadata.orm.proposals import Proposals
from pacifica.metadata.orm.users import Users
from pacifica.metadata.orm.base import DB
from pacifica.metadata.rest.orm import CherryPyAPI


class ProposalParticipant(CherryPyAPI):
    """
    Relates proposals and users objects.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | person            | Link to the Users model             |
        +-------------------+-------------------------------------+
        | proposal          | Link to the Proposals model         |
        +-------------------+-------------------------------------+
    """

    person = ForeignKeyField(Users, backref='proposals')
    proposal = ForeignKeyField(Proposals, backref='users')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('person', 'proposal')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(ProposalParticipant, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(
            self.__data__['proposal']), int(self.__data__['person']))
        obj['person_id'] = int(self.__data__['person'])
        obj['proposal_id'] = unicode_type(self.__data__['proposal'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(ProposalParticipant, self).from_hash(obj)
        self._set_only_if('person_id', obj, 'person',
                          lambda: Users.get(Users.id == obj['person_id']))
        self._set_only_if('proposal_id', obj, 'proposal',
                          lambda: Proposals.get(Proposals.id == obj['proposal_id']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(ProposalParticipant, cls).where_clause(kwargs)
        attrs = ['person', 'proposal']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
