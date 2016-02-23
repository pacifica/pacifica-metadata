#!/usr/bin/python
"""
Contains the Files object model primary unit of metadata for Pacifica.
"""
from datetime import datetime
from time import mktime
from peewee import ForeignKeyField, CharField, BigIntegerField
from peewee import DateTimeField, BooleanField, Expression, OP
from metadata.orm.base import PacificaModel
from metadata.orm.transactions import Transactions

class Files(PacificaModel):
    """
    Files metadata contains various attributes describing a file and where
    it came from.
    """
    file_id = BigIntegerField(default=-1, primary_key=True)
    name = CharField(default="")
    subdir = CharField(default="")
    vtime = DateTimeField(default=datetime.now)
    verified = BooleanField(default=False)
    size = BigIntegerField(default=-1)
    transaction = ForeignKeyField(Transactions, related_name='files')

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Files, self).to_hash()
        obj['file_id'] = int(self.file_id)
        obj['name'] = str(self.name)
        obj['subdir'] = str(self.subdir)
        obj['vtime'] = int(mktime(self.vtime.timetuple()))
        obj['verified'] = str(self.verified)
        obj['size'] = int(self.size)
        obj['transaction_id'] = int(self.transaction.transaction_id)

    def from_hash(self, obj):
        """
        Converts the hash to an object
        """
        super(Files, self).from_hash(obj)
        if 'file_id' in obj:
            self.file_id = int(obj['file_id'])
        if 'name' in obj:
            self.name = str(obj['name'])
        if 'subdir' in obj:
            self.subdir = str(obj['subdir'])
        if 'vtime' in obj:
            self.vtime = datetime.fromtimestamp(int(obj['vtime']))
        if 'verified' in obj:
            self.verified = bool(obj['verified'])
        if 'size' in obj:
            self.size = int(obj['size'])
        if 'transaction_id' in obj:
            self.transaction = Transactions.get(
                Transactions.transaction_id == obj['transaction_id']
            )

    def where_clause(self, kwargs):
        """
        PeeWee specific extension meant to be passed to a PeeWee get
        or select.
        """
        where_clause = super(Files, self).where_clause(kwargs)
        if 'vtime' in kwargs:
            kwargs['vtime'] = datetime.fromtimestamp(kwargs['vtime'])
        if 'verified' in kwargs:
            kwargs['verified'] = bool(kwargs['verified'])
        if 'transaction_id' in kwargs:
            kwargs['transaction_id'] = Transactions.get(
                Transactions.transaction_id == kwargs['transaction_id']
            )
        for key in ['file_id', 'name', 'subdir', 'size', 'vtime', 'verified'
                    'transaction_id']:
            if key in kwargs:
                where_clause &= Expression(Files.__dict__[key].field, OP.EQ, kwargs[key])
        return where_clause

