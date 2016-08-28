#!/usr/bin/python
"""
Contains model for groups
"""
from peewee import CharField, BooleanField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Groups(CherryPyAPI):
    """
    Groups model and associated fields.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | group_name        | name of the group                   |
        +-------------------+-------------------------------------+
        | is_admin          | does the group has admin abilities  |
        +-------------------+-------------------------------------+
        | author_precedence | encoding for the group_name         |
        +-------------------+-------------------------------------+
    """
    group_name = CharField(default="")
    is_admin = BooleanField(default=False)
    encoding = CharField(default="UTF8")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Groups, Groups).elastic_mapping_builder(obj)
        obj['group_name'] = obj['encoding'] = {'type': 'string'}
        obj['is_admin'] = {'type': 'boolean'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Groups, self).to_hash()
        obj['_id'] = int(self.id)
        obj['group_name'] = unicode(self.group_name)
        obj['encoding'] = str(self.encoding)
        obj['is_admin'] = bool(self.is_admin)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object.
        """
        super(Groups, self).from_hash(obj)
        # pylint: disable=invalid-name
        if '_id' in obj:
            self.id = int(obj['_id'])
        # pylint: enable=invalid-name
        if 'group_name' in obj:
            self.group_name = unicode(obj['group_name'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])
        if 'is_admin' in obj:
            self.is_admin = bool(obj['is_admin'])

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Groups, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Groups.id, OP.EQ, kwargs['_id'])
        for key in ['group_name', 'is_admin', 'encoding']:
            if key in kwargs:
                where_clause &= Expression(getattr(Groups, key), OP.EQ, kwargs[key])
        return where_clause
