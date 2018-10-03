#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Keywords linked to citations."""
from peewee import CharField, IntegerField, ForeignKeyField
from metadata.rest.orm import CherryPyAPI
from metadata.orm.users import Users
from metadata.orm.transactions import Transactions
from metadata.orm.utils import unicode_type


class DOIEntries(CherryPyAPI):
    """
    DOI Entries Model.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | doi_id            | OSTI identifier (postfix)           |
        +-------------------+-------------------------------------+
        | doi               | official DOI string                 |
        +-------------------+-------------------------------------+
        | transaction       | Corresponding transaction ID        |
        +-------------------+-------------------------------------+
        | status            | Current publishing status           |
        +-------------------+-------------------------------------+
        | creator           | Link to Users table                 |
        +-------------------+-------------------------------------+
    """

    doi_id = IntegerField(primary_key=True)
    doi = CharField()
    status = CharField(default='PENDING')
    site_url = CharField()
    transaction = ForeignKeyField(Transactions)
    creator = ForeignKeyField(Users, related_name='dois_created')

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(DOIEntries, DOIEntries).elastic_mapping_builder(obj)
        obj['doi_id'] = obj['creator'] = obj['transaction'] = {
            'type': 'integer'}
        obj['doi'] = obj['status'] = obj['site_url'] = \
            {'type': 'text', 'fields': {'keyword': {
                'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(DOIEntries, self).to_hash(**flags)
        obj['doi_id'] = int(
            self.doi_id) if self.doi_id is not None else obj['doi_id']
        obj['_id'] = obj['doi_id']
        obj['doi'] = unicode_type(self.doi)
        obj['status'] = unicode_type(self.status)
        obj['site_url'] = unicode_type(self.site_url)
        obj['transaction_id'] = int(self.__data__['transaction'])
        obj['creator_id'] = int(self.__data__['creator'])
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(DOIEntries, self).from_hash(obj)
        self._set_only_if('doi_id', obj, '_id', lambda: int(obj['doi_id']))
        self._set_only_if('doi_id', obj, 'doi_id', lambda: int(obj['doi_id']))
        self._set_only_if('doi', obj, 'doi',
                          lambda: unicode_type(obj['doi']))
        self._set_only_if('status', obj, 'status',
                          lambda: unicode_type(obj['status']))
        self._set_only_if('site_url', obj, 'site_url',
                          lambda: unicode_type(obj['site_url']))
        self._set_only_if('creator_id', obj, 'creator',
                          lambda: Users.get(Users.id == obj['creator_id']))
        self._set_only_if('transaction_id', obj, 'transaction',
                          lambda: Transactions.get(Transactions.id == obj['transaction_id']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(DOIEntries, cls).where_clause(kwargs)
        return cls._where_attr_clause(where_clause, kwargs, [
            'doi_id', 'doi', 'status', 'site_url', 'creator', 'transaction_id'])
