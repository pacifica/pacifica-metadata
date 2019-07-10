#!/usr/bin/python
# -*- coding: utf-8 -*-
"""DatasetFile links Datasets and Files objects."""
from peewee import ForeignKeyField, CompositeKey
from .base import DB
from .utils import index_hash
from .datasets import Datasets
from .files import Files
from ..rest.orm import CherryPyAPI


class DatasetFile(CherryPyAPI):
    """
    DatasetFile attributes are foreign keys.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | dataset           | Link to the Datasets model          |
        +-------------------+-------------------------------------+
        | file              | Link to the Files model             |
        +-------------------+-------------------------------------+
    """

    dataset = ForeignKeyField(Datasets, backref='datasets')
    file = ForeignKeyField(Files, backref='files')

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the database and the primary key."""

        database = DB
        primary_key = CompositeKey('dataset', 'file')
    # pylint: enable=too-few-public-methods

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(DatasetFile, self).to_hash(**flags)
        obj['_id'] = index_hash(int(self.__data__['dataset']),
                                int(self.__data__['file']))
        obj['dataset'] = int(self.__data__['dataset'])
        obj['file'] = int(self.__data__['file'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(DatasetFile, self).from_hash(obj)
        self._set_only_if('dataset', obj, 'dataset',
                          lambda: Datasets.get(Datasets.id == obj['dataset']))
        self._set_only_if('file', obj, 'file',
                          lambda: Files.get(Files.id == obj['file']))

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(DatasetFile, cls).where_clause(kwargs)
        attrs = ['dataset', 'file']
        return cls._where_attr_clause(where_clause, kwargs, attrs)
