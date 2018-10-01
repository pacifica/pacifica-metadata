#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Keywords linked to citations."""
from peewee import CharField, IntegerField, ForeignKeyField
from metadata.rest.orm import CherryPyAPI
from metadata.orm.doi_entries import DOIEntries
from metadata.orm.utils import unicode_type


class DOIAuthors(CherryPyAPI):
    """
    DOI Entries Model.

    Attributes:
        +-------------------+-----------------------------------------+
        | Name              | Description                             |
        +===================+=========================================+
        | doi_id            | OSTI identifier (postfix)               |
        +-------------------+-----------------------------------------+
        | author_order      | where does this author go in the order? |
        +-------------------+-----------------------------------------+
        | last_name         | Author last name                        |
        +-------------------+-----------------------------------------+
        | first_name        | Author first name                       |
        +-------------------+-----------------------------------------+
        | email             | Author email address                    |
        +-------------------+-----------------------------------------+
        | affiliation       | Institutional affiliation               |
        +-------------------+-----------------------------------------+
        | orcid             | Author's ORCID ID                       |
        +-------------------+-----------------------------------------+
    """

    doi_id = ForeignKeyField(DOIEntries, related_name='doi_authorships')
    author_order = IntegerField(default=1)
    last_name = CharField()
    first_name = CharField()
    email = CharField(null=True)
    affiliation = CharField(null=True)
    orcid = CharField(null=True)

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(DOIAuthors, DOIAuthors).elastic_mapping_builder(obj)
        obj['last_name'] = obj['first_name'] = obj['email'] = obj['affiliation'] = obj['orcid'] = \
            {'type': 'text', 'fields': {'keyword': {
                'type': 'keyword', 'ignore_above': 256}}}
        obj['author_order'] = obj['doi_id'] = {'type': 'integer'}

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(DOIAuthors, self).to_hash(**flags)
        obj['doi_id'] = int(self.__data__['doi_id'])
        obj['author_order'] = int(self.author_order)
        obj['last_name'] = unicode_type(self.last_name)
        obj['first_name'] = unicode_type(self.first_name)
        obj['email'] = unicode_type(self.email)
        obj['affiliation'] = unicode_type(self.affiliation)
        obj['orcid'] = unicode_type(self.orcid)
        return obj

    def from_hash(self, obj):
        """Convert the hash to the object."""
        super(DOIAuthors, self).from_hash(obj)
        self._set_only_if('doi_id', obj, 'doi_id', lambda: int(obj['doi_id']))
        self._set_only_if('author_order', obj, 'author_order',
                          lambda: int(obj['author_order']))
        self._set_only_if('last_name', obj, 'last_name',
                          lambda: unicode_type(obj['last_name']))
        self._set_only_if('first_name', obj, 'first_name',
                          lambda: unicode_type(obj['first_name']))
        self._set_only_if('email', obj, 'email',
                          lambda: unicode_type(obj['email']))
        self._set_only_if('affiliation', obj, 'affiliation',
                          lambda: unicode_type(obj['affiliation']))
        self._set_only_if('orcid', obj, 'orcid',
                          lambda: unicode_type(obj['orcid']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(DOIAuthors, cls).where_clause(kwargs)
        return cls._where_attr_clause(where_clause, kwargs, [
            'doi_id', 'author_order', 'last_name', 'first_name', 'email', 'affiliation', 'orcid'])
