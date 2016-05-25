#!/usr/bin/python
"""
Contains the Files object model primary unit of metadata for Pacifica.
"""
from datetime import datetime
from time import mktime
from peewee import ForeignKeyField, CharField, BigIntegerField
from peewee import DateTimeField, Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.transactions import Transactions

class Files(CherryPyAPI):
    """
    Files metadata contains various attributes describing a file and where
    it came from.
    """
    #pylint: disable=too-many-instance-attributes
    name = CharField(default="")
    subdir = CharField(default="")
    ctime = DateTimeField(default=datetime.now)
    mtime = DateTimeField(default=datetime.now)
    size = BigIntegerField(default=-1)
    transaction = ForeignKeyField(Transactions, related_name='files')
    #pylint: enable=too-many-instance-attributes

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Files, Files).elastic_mapping_builder(obj)
        obj['transaction_id'] = obj['size'] = \
        {'type': 'integer'}
        obj['ctime'] = obj['mtime'] = \
        {'type': 'date', 'format': 'epoch_second'}
        obj['name'] = obj['subdir'] = \
        {'type': 'string'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Files, self).to_hash()
        obj['_id'] = int(self.id)
        obj['name'] = str(self.name)
        obj['subdir'] = str(self.subdir)
        obj['ctime'] = int(mktime(self.ctime.timetuple()))
        obj['mtime'] = int(mktime(self.mtime.timetuple()))
        obj['size'] = int(self.size)
        obj['transaction_id'] = int(self.transaction.id)
        return obj

    def from_hash(self, obj):
        """
        Converts the hash to an object
        """
        super(Files, self).from_hash(obj)
        if '_id' in obj:
            # pylint: disable=invalid-name
            self.id = int(obj['_id'])
            # pylint: enable=invalid-name
        if 'name' in obj:
            self.name = str(obj['name'])
        if 'subdir' in obj:
            self.subdir = str(obj['subdir'])
        if 'ctime' in obj:
            self.ctime = datetime.fromtimestamp(int(obj['ctime']))
        if 'mtime' in obj:
            self.mtime = datetime.fromtimestamp(int(obj['mtime']))
        if 'size' in obj:
            self.size = int(obj['size'])
        if 'transaction_id' in obj:
            self.transaction = Transactions.get(
                Transactions.id == obj['transaction_id']
            )

    def where_clause(self, kwargs):
        """
        PeeWee specific extension meant to be passed to a PeeWee get
        or select.
        """
        where_clause = super(Files, self).where_clause(kwargs)
        for date in ['mtime', 'ctime']:
            if date in kwargs:
                kwargs[date] = datetime.fromtimestamp(kwargs[date])
        if 'transaction_id' in kwargs:
            kwargs['transaction_id'] = Transactions.get(
                Transactions.id == kwargs['transaction_id']
            )
        if '_id' in kwargs:
            where_clause &= Expression(Files.id, OP.EQ, kwargs['_id'])
        for key in ['name', 'subdir', 'size', 'mtime', 'ctime']:
            if key in kwargs:
                where_clause &= Expression(getattr(Files, key), OP.EQ, kwargs[key])
        return where_clause

