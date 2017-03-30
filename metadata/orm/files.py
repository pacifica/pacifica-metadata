#!/usr/bin/python
"""Contains the Files object model primary unit of metadata for Pacifica."""
from peewee import ForeignKeyField, CharField, BigIntegerField
from peewee import Expression, OP
from metadata.rest.orm import CherryPyAPI
from metadata.orm.transactions import Transactions
from metadata.orm.utils import datetime_now_nomicrosecond, ExtendDateTimeField
from metadata.orm.utils import unicode_type


# pylint: disable=too-many-instance-attributes
class Files(CherryPyAPI):
    """
    Files metadata.

    This object contains various attributes describing a file and where
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
        | hashsum     | Hash sum string                           |
        +-------------+-------------------------------------------+
        | hashtype    | Hash sum type string                      |
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

    name = CharField(default='')
    subdir = CharField(default='')
    ctime = ExtendDateTimeField(default=datetime_now_nomicrosecond)
    mtime = ExtendDateTimeField(default=datetime_now_nomicrosecond)
    hashsum = CharField(default='')
    hashtype = CharField(default='sha1')
    size = BigIntegerField(default=-1)
    transaction = ForeignKeyField(Transactions, related_name='files')
    mimetype = CharField(default='')
    encoding = CharField(default='UTF8')

    @staticmethod
    def elastic_mapping_builder(obj):
        """Build the elasticsearch mapping bits."""
        super(Files, Files).elastic_mapping_builder(obj)
        obj['transaction_id'] = obj['size'] = \
            {'type': 'integer'}
        obj['ctime'] = obj['mtime'] = \
            {'type': 'date', 'format': 'yyyy-mm-dd\'T\'HH:mm:ss'}
        obj['name'] = obj['subdir'] = obj['mimetype'] = \
            obj['encoding'] = obj['hashsum'] = \
            obj['hashtype'] = {'type': 'string'}

    def to_hash(self):
        """Convert the object to a hash."""
        obj = super(Files, self).to_hash()
        obj['_id'] = int(self.id)
        obj['name'] = unicode_type(self.name)
        obj['subdir'] = unicode_type(self.subdir)
        obj['mimetype'] = str(self.mimetype)
        # pylint: disable=no-member
        obj['ctime'] = self.ctime.isoformat()
        obj['mtime'] = self.mtime.isoformat()
        obj['transaction_id'] = int(self.transaction.id)
        # pylint: enable=no-member
        obj['size'] = int(self.size)
        obj['hashsum'] = str(self.hashsum)
        obj['hashtype'] = str(self.hashtype)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """Convert the hash to an object."""
        super(Files, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: int(obj['_id']))
        self._set_only_if('name', obj, 'name', lambda: unicode_type(obj['name']))
        self._set_only_if('subdir', obj, 'subdir', lambda: unicode_type(obj['subdir']))
        self._set_only_if('mimetype', obj, 'mimetype', lambda: str(obj['mimetype']))
        self._set_datetime_part('ctime', obj)
        self._set_datetime_part('mtime', obj)
        self._set_only_if('hashtype', obj, 'hashtype', lambda: str(obj['hashtype']))
        self._set_only_if('hashsum', obj, 'hashsum', lambda: str(obj['hashsum']))
        self._set_only_if('size', obj, 'size', lambda: int(obj['size']))
        self._set_only_if('encoding', obj, 'encoding', lambda: str(obj['encoding']))

        def trans_func():
            """Return the transaction for the obj id."""
            return Transactions.get(Transactions.id == obj['transaction_id'])
        self._set_only_if('transaction_id', obj, 'transaction', trans_func)

    def _where_date_clause(self, where_clause, kwargs):
        for date in ['mtime', 'ctime']:
            if date in kwargs:
                date_obj, date_oper = self._date_operator_compare(date, kwargs)
                where_clause &= Expression(getattr(Files, date), date_oper, date_obj)
        return where_clause

    @staticmethod
    def _where_attr_clause(where_clause, kwargs):
        for key in ['name', 'subdir', 'mimetype', 'size', 'encoding', 'hashtype', 'hashsum']:
            if key in kwargs:
                key_oper = OP.EQ
                if '{0}_operator'.format(key) in kwargs:
                    key_oper = getattr(OP, kwargs['{0}_operator'.format(key)].upper())
                where_clause &= Expression(getattr(Files, key), key_oper, kwargs[key])
        return where_clause

    def where_clause(self, kwargs):
        """PeeWee specific where expression."""
        where_clause = super(Files, self).where_clause(kwargs)
        if 'transaction_id' in kwargs:
            trans = Transactions.get(
                Transactions.id == kwargs['transaction_id']
            )
            where_clause &= Expression(Files.transaction, OP.EQ, trans)
        if '_id' in kwargs:
            where_clause &= Expression(Files.id, OP.EQ, kwargs['_id'])
        where_clause = self._where_date_clause(where_clause, kwargs)
        where_clause = self._where_attr_clause(where_clause, kwargs)
        return where_clause
