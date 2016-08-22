#!/usr/bin/python
"""
Users data model
"""
from peewee import CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Users(CherryPyAPI):
    """
    Users data model object
    """
    first_name = CharField(default="")
    last_name = CharField(default="")
    network_id = CharField(null=True)
    email_address = CharField(default="")
    encoding = CharField(default="UTF8")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Users, Users).elastic_mapping_builder(obj)
        obj['first_name'] = obj['last_name'] = obj['network_id'] = \
        obj['encoding'] = {'type': 'string'}

    def to_hash(self):
        """
        Convert the object to a hash
        """
        obj = super(Users, self).to_hash()
        obj['_id'] = int(self.id)
        obj['first_name'] = unicode(self.first_name)
        obj['last_name'] = unicode(self.last_name)
        if self.network_id is not None:
            obj['network_id'] = unicode(self.network_id.lower())
        else:
            obj['network_id'] = None
        obj['email_address'] = unicode(self.email_address)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object
        """
        super(Users, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = int(obj['_id'])
            # pylint: enable=invalid-name
        if 'first_name' in obj:
            self.first_name = unicode(obj['first_name'])
        if 'last_name' in obj:
            self.last_name = unicode(obj['last_name'])
        if 'network_id' in obj:
            self.network_id = unicode(obj['network_id'])
        if 'email_address' in obj:
            self.email_address = unicode(obj['email_address'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(Users, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Users.id, OP.EQ, kwargs['_id'])
        for key in ['first_name', 'last_name', 'network_id', 'encoding', 'email_address']:
            if key in kwargs:
                where_clause &= Expression(getattr(Users, key), OP.EQ, kwargs[key])
        return where_clause
