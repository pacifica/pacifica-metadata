#!/usr/bin/python
"""
Contributors model describes an author to a journal article.
"""
from peewee import IntegerField, TextField, CharField, Expression, OP
from metadata.orm.base import PacificaModel

class Contributors(PacificaModel):
    """
    Contributors object and associated fields.
    """
    author_id = IntegerField(default=-1, primary_key=True)
    first_name = CharField(default="")
    middle_initial = CharField(default="")
    last_name = CharField(default="")
    network_id = CharField(default="")
    dept_code = CharField(default="")
    institution_name = TextField(default="")

    def to_hash(self):
        """
        Convert the object fields into a serializable hash.
        """
        obj = super(Contributors, self).to_hash()
        obj['author_id'] = int(self.author_id)
        obj['first_name'] = str(self.first_name)
        obj['middle_initial'] = str(self.middle_initial)
        obj['last_name'] = str(self.last_name)
        obj['network_id'] = str(self.network_id)
        obj['dept_code'] = str(self.dept_code)
        obj['institution_name'] = str(self.institution_name)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object fields.
        """
        super(Contributors, self).from_hash(obj)
        if 'author_id' in obj:
            self.author_id = int(obj['author_id'])
        if 'first_name' in obj:
            self.first_name = str(obj['first_name'])
        if 'middle_initial' in obj:
            self.middle_initial = str(obj['middle_initial'])
        if 'last_name' in obj:
            self.last_name = str(obj['last_name'])
        if 'network_id' in obj:
            self.network_id = str(obj['network_id'])
        if 'dept_code' in obj:
            self.dept_code = str(obj['dept_code'])
        if 'institution_name' in obj:
            self.institution_name = str(obj['institution_name'])

    def where_clause(self, kwargs):
        """
        Generate the PeeWee where clause used in searching.
        """
        where_clause = super(Contributors, self).where_clause(kwargs)
        for key in ['author_id', 'first_name', 'last_name', 'network_id'
                    'middle_initial', 'dept_code', 'institution_name']:
            if key in kwargs:
                where_clause &= Expression(Contributors.__dict__[key].field, OP.EQ, kwargs[key])
        return where_clause


