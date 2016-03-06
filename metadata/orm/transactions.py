#!/usr/bin/python
"""
Transactions model
"""
from peewee import BigIntegerField, ForeignKeyField, BooleanField, Expression, OP
from metadata.orm.base import PacificaModel
from metadata.orm.users import Users

class Transactions(PacificaModel):
    """
    Transactions model class
    """
    transaction_id = BigIntegerField(default=-1, primary_key=True)
    verified = BooleanField(default=False)
    submitter = ForeignKeyField(Users, related_name='transactions')

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Transactions, self).to_hash()
        obj['transaction_id'] = int(self.transaction_id)
        obj['verified'] = str(self.verified)
        obj['submitter'] = int(self.submitter.person_id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash into the object
        """
        super(Transactions, self).from_hash(obj)
        if 'transaction_id' in obj:
            self.transaction_id = int(obj['transaction_id'])
        if 'submitter' in obj:
            self.submitter = Users.get(Users.person_id == obj['submitter'])
        if 'verified' in obj:
            self.verified = bool(str(obj['verified']) == "True")

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(Transactions, self).where_clause(kwargs)
        if 'transaction_id' in kwargs:
            where_clause &= Expression(Transactions.transaction_id, OP.EQ, kwargs['transaction_id'])
        if 'submitter' in kwargs:
            user = Users.get(Users.person_id == kwargs['submitter'])
            where_clause &= Expression(Transactions.submitter, OP.EQ, user)
        if 'verified' in kwargs:
            verified = bool(str(kwargs['verified']) == "True")
            where_clause &= Expression(Transactions.verified, OP.EQ, verified)
        return where_clause
