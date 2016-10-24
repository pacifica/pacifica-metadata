#!/usr/bin/python
"""
Contains the Files object model primary unit of metadata for Pacifica.
"""
from datetime import datetime
from time import mktime
from peewee import ForeignKeyField, CharField, BigIntegerField
from peewee import Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.transactions import Transactions
from metadata.orm.utils import datetime_now_nomicrosecond, ExtendDateTimeField

#pylint: disable=too-many-instance-attributes
class Files(CherryPyAPI):
    """
    Files metadata contains various attributes describing a file and where
    it came from.

    Attributes:
        +-------------+-------------------------------------------+
        | Name        | Description                               |
        +=============+===========================================+
        | name        | Name of the file                          |
        +-------------+-------------------------------------------+
        | subdir      | Subdirectory the file is in               |
        +-------------+-------------------------------------------+
        | ctime       | Creation time for the file                |
        +-------------+-------------------------------------------+
        | mtime       | User modified time for the file           |
        +-------------+-------------------------------------------+
        | size        | Size of the file in bytes                 |
        +-------------+-------------------------------------------+
        | transaction | Link to the transaction model             |
        +-------------+-------------------------------------------+
        | mimetype    | mimetype of the file, if any              |
        +-------------+-------------------------------------------+
        | encoding    | encoding in the file name or subdir field |
        +-------------+-------------------------------------------+
    """
    name = CharField(default="")
    subdir = CharField(default="")
    ctime = ExtendDateTimeField(default=datetime_now_nomicrosecond)
    mtime = ExtendDateTimeField(default=datetime_now_nomicrosecond)
    size = BigIntegerField(default=-1)
    transaction = ForeignKeyField(Transactions, related_name='files')
    mimetype = CharField(default="")
    encoding = CharField(default="UTF8")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Files, Files).elastic_mapping_builder(obj)
        obj['transaction_id'] = obj['size'] = \
        {'type': 'integer'}
        obj['ctime'] = obj['mtime'] = \
        {'type': 'date', 'format': "yyyy-mm-dd'T'HH:mm:ss"}
        obj['name'] = obj['subdir'] = obj['mimetype'] = \
        obj['encoding'] = {'type': 'string'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Files, self).to_hash()
        obj['_id'] = int(self.id)
        obj['name'] = unicode(self.name)
        obj['subdir'] = unicode(self.subdir)
        obj['mimetype'] = str(self.mimetype)
        obj['ctime'] = int(mktime(self.ctime.timetuple()))
        obj['mtime'] = int(mktime(self.mtime.timetuple()))
        obj['size'] = int(self.size)
        obj['transaction_id'] = int(self.transaction.id)
        obj['encoding'] = str(self.encoding)
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
            self.name = unicode(obj['name'])
        if 'subdir' in obj:
            self.subdir = unicode(obj['subdir'])
        if 'mimetype' in obj:
            self.mimetype = str(obj['mimetype'])
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
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])

    def where_clause(self, kwargs):
        """
        PeeWee specific extension meant to be passed to a PeeWee get
        or select.
        """
        where_clause = super(Files, self).where_clause(kwargs)
        if 'transaction_id' in kwargs:
            kwargs['transaction_id'] = Transactions.get(
                Transactions.id == kwargs['transaction_id']
            )
        if '_id' in kwargs:
            where_clause &= Expression(Files.id, OP.EQ, kwargs['_id'])
        for date in ['mtime', 'ctime']:
            if date in kwargs:
                date_obj, date_oper = self._date_operator_compare(date, kwargs)
                where_clause &= Expression(getattr(Files, date), date_oper, date_obj)
        for key in ['name', 'subdir', 'mimetype', 'size', 'encoding']:
            if key in kwargs:
                key_oper = OP.EQ
                if "%s_operator"%(key) in kwargs:
                    key_oper = getattr(OP, kwargs["%s_operator"%(key)])
                where_clause &= Expression(getattr(Files, key), key_oper, kwargs[key])
        return where_clause
