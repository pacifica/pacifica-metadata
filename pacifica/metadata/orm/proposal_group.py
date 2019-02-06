#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Proposal group relationship."""
from peewee import ForeignKeyField, CompositeKey
from pacifica.metadata.orm.utils import index_hash, unicode_type
from pacifica.metadata.orm.proposals import Proposals
from pacifica.metadata.orm.groups import Groups
from pacifica.metadata.orm.base import DB
from pacifica.metadata.rest.orm import CherryPyAPI


class ProposalGroup(CherryPyAPI):
    """
    Relates proposals and groups objects.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | group             | Link to the Group model             |
        +-------------------+-------------------------------------+
        | proposal          | Link to the Proposal model          |
        +-------------------+-------------------------------------+
    """

    group = ForeignKeyField(Groups, backref='proposals')
    proposal = ForeignKeyField(Proposals, backref='groups')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('group', 'proposal')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(ProposalGroup, self).to_hash(**flags)
        obj['_id'] = index_hash(unicode_type(
            self.__data__['proposal']), int(self.__data__['group']))
        obj['group_id'] = int(self.__data__['group'])
        obj['proposal_id'] = unicode_type(self.__data__['proposal'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(ProposalGroup, self).from_hash(obj)
        self._set_only_if(
            'proposal_id', obj, 'proposal',
            lambda: Proposals.get(Proposals.id == obj['proposal_id'])
        )
        self._set_only_if(
            'group_id', obj, 'group',
            lambda: Groups.get(Groups.id == obj['group_id'])
        )

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(ProposalGroup, cls).where_clause(kwargs)
        attrs = ['group', 'proposal']
        for attr in attrs:
            if '{}_id'.format(attr) in kwargs:
                kwargs[attr] = kwargs.pop('{}_id'.format(attr))
        return cls._where_attr_clause(where_clause, kwargs, attrs)
