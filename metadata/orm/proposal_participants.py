#!/usr/bin/python
"""
Proposal person relationship
"""
from peewee import ForeignKeyField, CharField, Expression, OP, CompositeKey
from metadata.orm.proposals import Proposals
from metadata.orm.users import Users
from metadata.orm.base import DB, PacificaModel

class ProposalParticipants(PacificaModel):
    """
    Relates proposals and users objects.
    """
    member = ForeignKeyField(Users, related_name='proposals')
    proposal = ForeignKeyField(Proposals, related_name='members')
    proposal_author_sw = CharField(default="")
    proposal_co_author_sw = CharField(default="")

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        PeeWee meta class contains the database and the primary key.
        """
        database = DB
        primary_key = CompositeKey('proposal_id', 'person_id')
    # pylint: enable=too-few-public-methods

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(ProposalParticipants, self).to_hash()
        obj['person_id'] = int(self.member.person_id)
        obj['proposal_id'] = int(self.proposal.proposal_id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash into the object
        """
        super(ProposalParticipants, self).from_hash(obj)
        if 'person_id' in obj:
            self.member = Users.get(Users.person_id == obj['person_id'])
        if 'proposal_id' in obj:
            self.proposal = Proposals.get(Proposals.proposal_id == obj['proposal_id'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(ProposalParticipants, self).where_clause(kwargs)
        if 'person_id' in kwargs:
            member = Users.get(Users.person_id == kwargs['person_id'])
            where_clause &= Expression(ProposalParticipants, OP.EQ, member)
        if 'proposal_id' in kwargs:
            proposal = Proposals.get(Proposals.proposal_id == kwargs['proposal_id'])
            where_clause &= Expression(ProposalParticipants.proposal, OP.EQ, proposal)
        return where_clause
