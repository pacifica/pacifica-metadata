#!/usr/bin/python
"""
FileKeyValue links Files and Keys and Values objects.
"""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.base import DB, PacificaModel
from metadata.orm.files import Files
from metadata.orm.values import Values
from metadata.orm.keys import Keys

class FileKeyValue(PacificaModel):
    """
    FileKeyValue attributes are foreign keys.
    """
    file = ForeignKeyField(Files, related_name='metadata')
    key = ForeignKeyField(Keys, related_name='metadata')
    value = ForeignKeyField(Values, related_name='metadata')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        PeeWee meta class contains the database and the primary key.
        """
        database = DB
        primary_key = CompositeKey('file', 'key', 'value')
    # pylint: enable=too-few-public-methods

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(FileKeyValue, self).to_hash()
        obj['file_id'] = int(self.file.file_id)
        obj['key_id'] = int(self.key.key_id)
        obj['value_id'] = int(self.value.value_id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash into the object
        """
        super(FileKeyValue, self).from_hash(obj)
        if 'file_id' in obj:
            self.file = Files.get(Files.file_id == obj['file_id'])
        if 'key_id' in obj:
            self.key = Keys.get(Keys.key_id == obj['key_id'])
        if 'value_id' in obj:
            self.value = Values.get(Values.value_id == obj['value_id'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(FileKeyValue, self).where_clause(kwargs)
        for key in ['file_id', 'key_id', 'value_id']:
            if key in kwargs:
                where_clause &= Expression(FileKeyValue.__dict__[key].field, OP.EQ, kwargs[key])
        return where_clause

