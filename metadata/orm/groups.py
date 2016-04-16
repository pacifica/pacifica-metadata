#!/usr/bin/python
"""
Contains model for groups
"""
from peewee import IntegerField, CharField, Boolean, Expression, OP
from metadata.orm.base import PacificaModel

class Groups(PacificaModel):
    """
    Groups model and associated fields.
    """
    group_id = IntegerField(default=-1, primary_key=True)
    group_name = CharField(default="")
    is_admin = BooleanField(default=False)

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Groups, self).to_hash()
        obj['group_id'] = int(self.group_id)
        obj['group_name'] = str(self.group_name)
        obj['is_admin'] = str(self.is_admin)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object.
        """
        super(Groups, self).from_hash(obj)
        if 'group_id' in obj:
            self.group_id = int(obj['group_id'])
        if 'group_name' in obj:
            self.group_name = str(obj['group_name'])
        if 'is_admin' in obj:
            self.is_admin = bool(obj['is_admin'])

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Groups, self).where_clause(kwargs)
        for key in ['group_id', 'group_name', 'is_admin']:
            if key in kwargs:
                where_clause &= Expression(getattr(Groups, key), OP.EQ, kwargs[key])
        return where_clause

