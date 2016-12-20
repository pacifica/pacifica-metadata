#!/usr/bin/python
"""Contains model for groups."""
from peewee import CharField, BooleanField, Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.utils import unicode_type


class Groups(CherryPyAPI):
    """
    Groups model and associated fields.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | name              | name of the group                   |
        +-------------------+-------------------------------------+
        | is_admin          | does the group has admin abilities  |
        +-------------------+-------------------------------------+
        | encoding          | encoding for the group name         |
        +-------------------+-------------------------------------+
    """

    name = CharField(default='')
    is_admin = BooleanField(default=False)
    encoding = CharField(default='UTF8')

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(Groups, Groups).elastic_mapping_builder(obj)
        obj['name'] = obj['encoding'] = {'type': 'string'}
        obj['is_admin'] = {'type': 'boolean'}

    def to_hash(self):
        """Convert the object to a hash."""
        obj = super(Groups, self).to_hash()
        obj['_id'] = int(self.id)
        obj['name'] = unicode_type(self.name)
        obj['encoding'] = str(self.encoding)
        obj['is_admin'] = bool(self.is_admin)
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(Groups, self).from_hash(obj)
        # pylint: disable=invalid-name
        if '_id' in obj:
            self.id = int(obj['_id'])
        # pylint: enable=invalid-name
        if 'name' in obj:
            self.name = unicode_type(obj['name'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])
        if 'is_admin' in obj:
            self.is_admin = self._bool_translate(obj['is_admin'])

    @staticmethod
    def _where_attr_clause(where_clause, kwargs):
        for key in ['name', 'is_admin', 'encoding']:
            if key in kwargs:
                key_oper = OP.EQ
                if '{0}_operator'.format(key) in kwargs:
                    key_oper = getattr(OP, kwargs['{0}_operator'.format(key)].upper())
                where_clause &= Expression(getattr(Groups, key), key_oper, kwargs[key])
        return where_clause

    def where_clause(self, kwargs):
        """PeeWee specific where clause used for search."""
        where_clause = super(Groups, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Groups.id, OP.EQ, kwargs['_id'])
        if 'is_admin' in kwargs:
            kwargs['is_admin'] = self._bool_translate(kwargs['is_admin'])
        return self._where_attr_clause(where_clause, kwargs)
