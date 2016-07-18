#!/usr/bin/python
"""
Contains model for groups
"""
from peewee import CharField, BooleanField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Groups(CherryPyAPI):
    """
    Groups model and associated fields.
    """
    group_name = CharField(default="")
    is_admin = BooleanField(default=False)

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Groups, Groups).elastic_mapping_builder(obj)
        obj['group_name'] = {'type': 'string'}
        obj['is_admin'] = {'type': 'boolean'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Groups, self).to_hash()
        obj['_id'] = int(self.id)
        obj['group_name'] = str(self.group_name)
        obj['is_admin'] = bool(self.is_admin)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object.
        """
        super(Groups, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = int(obj['_id'])
            # pylint: enable=invalid-name
        if 'group_name' in obj:
            self.group_name = str(obj['group_name'])
        if 'is_admin' in obj:
            self.is_admin = bool(obj['is_admin'])

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Groups, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Groups.id, OP.EQ, kwargs['_id'])
        for key in ['group_name', 'is_admin']:
            if key in kwargs:
                where_clause &= Expression(getattr(Groups, key), OP.EQ, kwargs[key])
        return where_clause
