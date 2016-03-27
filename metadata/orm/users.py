#!/usr/bin/python
"""
Users data model
"""
from peewee import IntegerField, CharField, Expression, OP
from metadata.orm.base import PacificaModel

class Users(PacificaModel):
    """
    Users data model object
    """
    person_id = IntegerField(default=-1, primary_key=True)
    first_name = CharField(default="")
    last_name = CharField(default="")
    network_id = CharField(default="")

    def to_hash(self):
        """
        Convert the object to a hash
        """
        obj = super(Users, self).to_hash()
        obj['person_id'] = self.person_id
        obj['first_name'] = self.first_name
        obj['last_name'] = self.last_name
        obj['network_id'] = self.network_id
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object
        """
        super(Users, self).from_hash(obj)
        if 'person_id' in obj:
            self.person_id = int(obj['person_id'])
        if 'first_name' in obj:
            self.first_name = obj['first_name']
        if 'last_name' in obj:
            self.last_name = obj['last_name']
        if 'network_id' in obj:
            self.network_id = obj['network_id']

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(Users, self).where_clause(kwargs)
        for key in ['person_id', 'first_name', 'last_name', 'network_id']:
            if key in kwargs:
                where_clause &= Expression(getattr(Users, key), OP.EQ, kwargs[key])
        return where_clause

