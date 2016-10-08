#!/usr/bin/python
"""
TransactionKeyValue links Transactions and Keys and Values objects.
"""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.base import DB
from metadata.orm.utils import index_hash
from metadata.orm.proposals import Proposals
from metadata.orm.analytical_tools import AnalyticalTools
from metadata.rest.orm import CherryPyAPI

class AToolProposal(CherryPyAPI):
    """
    TransactionKeyValue attributes are foreign keys.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | proposal          | Link to the Proposals model         |
        +-------------------+-------------------------------------+
        | analytical_tool   | Link to the AnalyticalTools model   |
        +-------------------+-------------------------------------+
    """
    proposal = ForeignKeyField(Proposals, related_name='atools')
    analytical_tool = ForeignKeyField(AnalyticalTools, related_name='proposals')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        PeeWee meta class contains the database and the primary key.
        """
        database = DB
        primary_key = CompositeKey('analytical_tool', 'proposal')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(AToolProposal, AToolProposal).elastic_mapping_builder(obj)
        obj['proposal_id'] = {'type': 'string'}
        obj['analytical_tool_id'] = {'type': 'integer'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(AToolProposal, self).to_hash()
        obj['_id'] = index_hash(self.proposal.id,
                                int(self.analytical_tool.id))
        obj['proposal_id'] = str(self.proposal.id)
        obj['analytical_tool_id'] = int(self.analytical_tool.id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash into the object
        """
        super(AToolProposal, self).from_hash(obj)
        if 'proposal_id' in obj:
            self.proposal = Proposals.get(Proposals.id == obj['proposal_id'])
        if 'analytical_tool_id' in obj:
            self.analytical_tool = AnalyticalTools.get(
                AnalyticalTools.id == obj['analytical_tool_id']
            )

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(AToolProposal, self).where_clause(kwargs)
        if 'proposal_id' in kwargs:
            prop = Proposals.get(Proposals.id == kwargs['proposal_id'])
            where_clause &= Expression(AToolProposal.proposal, OP.EQ, prop)
        if 'analytical_tool_id' in kwargs:
            atool = AnalyticalTools.get(AnalyticalTools.id == kwargs['analytical_tool_id'])
            where_clause &= Expression(AToolProposal.analytical_tool, OP.EQ, atool)
        return where_clause
