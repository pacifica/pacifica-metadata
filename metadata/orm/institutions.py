#!/usr/bin/python
"""
Describes an institution and its attributes.
"""
from peewee import IntegerField, TextField, CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Institutions(CherryPyAPI):
    """
    Institution model scribes an institute.
    """
    institution_id = IntegerField(default=-1, primary_key=True)
    institution_name = TextField(default="")
    association_cd = CharField(default="UNK")
    is_foreign = IntegerField(default=0)

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Institutions, self).to_hash()
        obj['institution_id'] = int(self.institution_id)
        obj['institution_name'] = str(self.institution_name)
        obj['association_cd'] = str(self.association_cd)
        obj['is_foreign'] = bool(self.is_foreign)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object.
        """
        super(Institutions, self).from_hash(obj)
        if 'institution_id' in obj:
            self.institution_id = int(obj['institution_id'])
        if 'institution_name' in obj:
            self.institution_name = str(obj['institution_name'])
        if 'association_cd' in obj:
            self.association_cd = str(obj['association_cd'])
        if 'is_foreign' in obj:
            self.is_foreign = bool(obj['is_foreign'])

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Institutions, self).where_clause(kwargs)
        for key in ['institution_id', 'institution_name', 'is_foreign',
                    'association_cd']:
            if key in kwargs:
                where_clause &= Expression(getattr(Institutions, key), OP.EQ, kwargs[key])
        return where_clause

