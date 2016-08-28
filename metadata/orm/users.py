#!/usr/bin/python
"""
Users data model
"""
from peewee import CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Users(CherryPyAPI):
    """
    Users data model object

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
    first_name = CharField(default="")
    middle_initial = CharField(default="")
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
        obj['middle_initial'] = obj['encoding'] = {'type': 'string'}

    def to_hash(self):
        """
        Convert the object to a hash
        """
        obj = super(Users, self).to_hash()
        obj['_id'] = int(self.id)
        obj['first_name'] = unicode(self.first_name)
        obj['middle_initial'] = unicode(self.middle_initial)
        obj['last_name'] = unicode(self.last_name)
        if self.network_id is not None:
            obj['network_id'] = unicode(self.network_id).lower()
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
        for attr in ['first_name', 'middle_initial', 'last_name', 'network_id', 'email_address']:
            if attr in obj:
                setattr(self, attr, unicode(obj[attr]))
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(Users, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Users.id, OP.EQ, kwargs['_id'])
        for key in ['first_name', 'middle_initial', 'last_name', 'network_id',
                    'encoding', 'email_address']:
            if key in kwargs:
                where_clause &= Expression(getattr(Users, key), OP.EQ, kwargs[key])
        return where_clause
