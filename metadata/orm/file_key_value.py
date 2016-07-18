#!/usr/bin/python
"""
FileKeyValue links Files and Keys and Values objects.
"""
from peewee import ForeignKeyField, CompositeKey, Expression, OP
from metadata.orm.base import DB
from metadata.orm.utils import index_hash
from metadata.orm.files import Files
from metadata.orm.values import Values
from metadata.orm.keys import Keys
from metadata.rest.orm import CherryPyAPI

class FileKeyValue(CherryPyAPI):
    """
    FileKeyValue attributes are foreign keys.
    """
    file = ForeignKeyField(Files, related_name='metadata')
    key = ForeignKeyField(Keys, related_name='file_links')
    value = ForeignKeyField(Values, related_name='file_links')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        PeeWee meta class contains the database and the primary key.
        """
        database = DB
        primary_key = CompositeKey('file', 'key', 'value')
    # pylint: enable=too-few-public-methods

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(FileKeyValue, FileKeyValue).elastic_mapping_builder(obj)
        obj['file_id'] = obj['key_id'] = obj['value_id'] = \
        {'type': 'integer'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(FileKeyValue, self).to_hash()
        obj['_id'] = index_hash(int(self.key.id),
                                int(self.file.id),
                                int(self.value.id))
        obj['file_id'] = int(self.file.id)
        obj['key_id'] = int(self.key.id)
        obj['value_id'] = int(self.value.id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash into the object
        """
        super(FileKeyValue, self).from_hash(obj)
        if 'file_id' in obj:
            self.file = Files.get(Files.id == obj['file_id'])
        if 'key_id' in obj:
            self.key = Keys.get(Keys.id == obj['key_id'])
        if 'value_id' in obj:
            self.value = Values.get(Values.id == obj['value_id'])

    def where_clause(self, kwargs):
        """
        Where clause for the various elements.
        """
        where_clause = super(FileKeyValue, self).where_clause(kwargs)
        if 'file_id' in kwargs:
            file_ = Files.get(Files.id == kwargs['file_id'])
            where_clause &= Expression(FileKeyValue.file, OP.EQ, file_)
        if 'key_id' in kwargs:
            key = Keys.get(Keys.id == kwargs['key_id'])
            where_clause &= Expression(FileKeyValue.key, OP.EQ, key)
        if 'value_id' in kwargs:
            value = Values.get(Values.id == kwargs['value_id'])
            where_clause &= Expression(FileKeyValue.value, OP.EQ, value)
        return where_clause
