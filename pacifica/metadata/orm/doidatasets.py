#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Keywords linked to citations."""
from peewee import CharField, ForeignKeyField
from pacifica.metadata.rest.orm import CherryPyAPI
from pacifica.metadata.orm.users import Users
from pacifica.metadata.orm.utils import unicode_type


class DOIDataSets(CherryPyAPI):
    """
    Keywords Model.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | doi               | official DOI string                 |
        +-------------------+-------------------------------------+
        | name              | name for the DOI                    |
        +-------------------+-------------------------------------+
        | encoding          | encoding of the keyword             |
        +-------------------+-------------------------------------+
    """

    doi = CharField(primary_key=True)
    name = CharField(default='')
    encoding = CharField(default='UTF8')
    creator = ForeignKeyField(Users, related_name='dois_created')

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(DOIDataSets, DOIDataSets).elastic_mapping_builder(obj)
        obj['creator'] = {'type': 'integer'}
        obj['doi'] = obj['name'] = obj['encoding'] = \
            {'type': 'text', 'fields': {'keyword': {
                'type': 'keyword', 'ignore_above': 256}}}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(DOIDataSets, self).to_hash(**flags)
        obj['_id'] = int(self.id) if self.id is not None else obj['_id']
        obj['doi'] = unicode_type(self.doi)
        obj['name'] = unicode_type(self.name)
        obj['creator'] = int(self.__data__['creator'])
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(DOIDataSets, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: int(obj['_id']))
        self._set_only_if('doi', obj, 'doi',
                          lambda: unicode_type(obj['doi']))
        self._set_only_if('name', obj, 'name',
                          lambda: unicode_type(obj['name']))
        self._set_only_if('creator', obj, 'creator',
                          lambda: Users.get(Users.id == obj['creator']))
        self._set_only_if('encoding', obj, 'encoding',
                          lambda: str(obj['encoding']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(DOIDataSets, cls).where_clause(kwargs)
        return cls._where_attr_clause(where_clause, kwargs, ['doi', 'name', 'encoding', 'creator'])
