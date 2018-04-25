#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Proposal person relationship."""
from peewee import ForeignKeyField, Expression, OP, CompositeKey
from metadata.orm.utils import index_hash, unicode_type
from metadata.orm.proposals import Proposals
from metadata.orm.users import Users
from metadata.orm.base import DB
from metadata.rest.orm import CherryPyAPI


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

    person = ForeignKeyField(Users, related_name='proposals')
    proposal = ForeignKeyField(Proposals, related_name='users')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('person', 'proposal')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(ProposalParticipant, ProposalParticipant).elastic_mapping_builder(obj)
        obj['person_id'] = {'type': 'integer'}
        obj['proposal_id'] = {'type': 'text', 'fields': {
            'keyword': {'type': 'keyword', 'ignore_above': 256}}}

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
        if 'person_id' in obj:
            self.person = Users.get(Users.id == obj['person_id'])
        if 'proposal_id' in obj:
            self.proposal = Proposals.get(Proposals.id == obj['proposal_id'])

    def where_clause(self, kwargs):
        """Where clause for the various elements."""
        where_clause = super(ProposalParticipant, self).where_clause(kwargs)
        if 'person_id' in kwargs:
            member = int(kwargs['person_id'])
            where_clause &= Expression(
                ProposalParticipant.person, OP.EQ, member)
        if 'proposal_id' in kwargs:
            proposal = kwargs['proposal_id']
            where_clause &= Expression(
                ProposalParticipant.proposal, OP.EQ, proposal)
        return where_clause
