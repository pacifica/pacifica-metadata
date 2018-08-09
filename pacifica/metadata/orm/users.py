#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Users data model."""
from peewee import CharField, Expression, OP
from pacifica.metadata.rest.orm import CherryPyAPI
from pacifica.metadata.orm.utils import unicode_type


class Users(CherryPyAPI):
    """
    Users data model object.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | first_name        | first name of the user/person       |
        +-------------------+-------------------------------------+
        | middle_initial    | middle initial of the user/person   |
        +-------------------+-------------------------------------+
        | last_name         | last name of the user/person        |
        +-------------------+-------------------------------------+
        | network_id        | computer account of the user/person |
        +-------------------+-------------------------------------+
        | email_address     | user/person email address           |
        +-------------------+-------------------------------------+
        | encoding          | encoding for the other attrs        |
        +-------------------+-------------------------------------+
    """

    first_name = CharField(default='', index=True)
    middle_initial = CharField(default='', index=True)
    last_name = CharField(default='', index=True)
    network_id = CharField(null=True, index=True)
    email_address = CharField(default='', index=True)
    encoding = CharField(default='UTF8')

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(Users, Users).elastic_mapping_builder(obj)
        obj['first_name'] = obj['last_name'] = obj['network_id'] = \
            obj['middle_initial'] = obj['encoding'] = \
            {'type': 'text', 'fields': {'keyword': {
                'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(Users, self).to_hash(**flags)
        obj['_id'] = int(self.id)
        obj['first_name'] = unicode_type(self.first_name)
        obj['middle_initial'] = unicode_type(self.middle_initial)
        obj['last_name'] = unicode_type(self.last_name)
        if self.network_id is not None:
            obj['network_id'] = unicode_type(self.network_id).lower()
        else:
            obj['network_id'] = None
        obj['email_address'] = unicode_type(self.email_address)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(Users, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: int(obj['_id']))
        for attr in ['first_name', 'middle_initial', 'last_name', 'email_address']:
            # pylint: disable=cell-var-from-loop
            self._set_only_if(attr, obj, attr, lambda: unicode_type(obj[attr]))
            # pylint: enable=cell-var-from-loop
        self._set_only_if('network_id', obj, 'network_id',
                          lambda: unicode_type(obj['network_id']).lower())
        self._set_only_if('encoding', obj, 'encoding',
                          lambda: str(obj['encoding']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(Users, cls).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Users.id, OP.EQ, kwargs['_id'])
        if 'network_id' in kwargs:
            kwargs['network_id'] = kwargs['network_id'].lower()
        return cls._where_attr_clause(
            where_clause,
            kwargs,
            [
                'first_name',
                'middle_initial',
                'last_name',
                'network_id',
                'encoding',
                'email_address'
            ]
        )
